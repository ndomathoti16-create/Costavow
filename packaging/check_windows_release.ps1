param([string]$ArchivePath = 'dist\Costavow-Windows-x64.zip')
$ErrorActionPreference = 'Stop'
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class CostavowWindowProbe {
    public delegate bool Visitor(IntPtr window, IntPtr state);
    [DllImport("user32.dll")] public static extern bool EnumWindows(Visitor visitor, IntPtr state);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr window, out uint process);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr window, StringBuilder text, int count);
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr window, uint message, IntPtr wparam, IntPtr lparam);
}
"@
$testRoot = Join-Path (Resolve-Path 'build') ('windows-download-' + [guid]::NewGuid().ToString('N'))
Expand-Archive -LiteralPath $ArchivePath -DestinationPath $testRoot
$executable = Join-Path $testRoot 'Costavow.exe'
if (!(Test-Path -LiteralPath $executable) -or (Test-Path (Join-Path $testRoot '_internal'))) {
    throw 'The release must contain a single executable with embedded runtime libraries.'
}
# Simulate Explorer preserving the Internet mark on files from a downloaded ZIP.
Get-ChildItem -LiteralPath $testRoot -File | ForEach-Object {
    Set-Content -LiteralPath $_.FullName -Stream Zone.Identifier -Value "[ZoneTransfer]`r`nZoneId=3"
}
$previousDataDir = $env:COSTAVOW_USER_DATA_DIR
$env:COSTAVOW_USER_DATA_DIR = Join-Path $testRoot 'test-state'
$ownedIds = [System.Collections.Generic.HashSet[int]]::new()
try {
    # Redirected streams use CreateProcess: test the runtime after launch, not the shell trust prompt.
    # The Internet mark remains intact; normal Explorer launches retain Windows' publisher checks.
    $launcher = Start-Process -FilePath $executable -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $testRoot 'launcher.stdout.log') `
        -RedirectStandardError (Join-Path $testRoot 'launcher.stderr.log')
    [void]$ownedIds.Add($launcher.Id)
    $deadline = (Get-Date).AddSeconds(90)
    $script:window = [IntPtr]::Zero
    while ((Get-Date) -lt $deadline -and !$launcher.HasExited) {
        $processes = @(Get-CimInstance Win32_Process)
        do {
            $oldCount = $ownedIds.Count
            foreach ($item in $processes) {
                if ($ownedIds.Contains([int]$item.ParentProcessId)) { [void]$ownedIds.Add([int]$item.ProcessId) }
            }
        } while ($ownedIds.Count -gt $oldCount)
        # Hidden CI windows have no Process.MainWindowHandle; inspect only this launch's windows.
        $script:window = [IntPtr]::Zero
        [void][CostavowWindowProbe]::EnumWindows({
            param($handle, $state)
            [uint32]$windowOwner = 0
            [void][CostavowWindowProbe]::GetWindowThreadProcessId($handle, [ref]$windowOwner)
            if ($ownedIds.Contains([int]$windowOwner)) {
                $title = [System.Text.StringBuilder]::new(256)
                [void][CostavowWindowProbe]::GetWindowText($handle, $title, $title.Capacity)
                if ($title.ToString() -like 'Costavow*FinOps Decision Evidence*') {
                    $script:window = $handle
                    return $false
                }
            }
            return $true
        }, [IntPtr]::Zero)
        if ($window -ne [IntPtr]::Zero) { break }
        Start-Sleep -Milliseconds 250
    }
    if ($window -eq [IntPtr]::Zero) { throw 'The downloaded executable did not open its native application window.' }
    if (!(Get-Content -LiteralPath $executable -Stream Zone.Identifier).Contains('ZoneId=3')) {
        throw 'The executable lost its Windows download-origin mark during the test.'
    }
    if (!(Get-ChildItem -LiteralPath $testRoot -Filter THIRD_PARTY_LICENSES.txt)) {
        throw 'Readable third-party licenses are missing from the ZIP.'
    }
    if (Test-Path (Join-Path $testRoot 'test-state\logs\desktop-crash.log')) {
        throw 'The native launch generated a crash report.'
    }
    if (![CostavowWindowProbe]::PostMessage($window, 0x10, [IntPtr]::Zero, [IntPtr]::Zero)) { throw 'The native window did not accept a normal close.' }
    if (!$launcher.WaitForExit(15000)) { throw 'The app did not shut down after closing the window.' }
    if ($launcher.ExitCode -ne 0) { throw "The application exited with code $($launcher.ExitCode)." }
    Write-Output 'PASS: Internet-marked executable opened its native window and closed cleanly.'
} finally {
    # Only processes descended from the test executable are eligible for cleanup.
    foreach ($ownedId in $ownedIds) { Stop-Process -Id $ownedId -ErrorAction SilentlyContinue }
    $env:COSTAVOW_USER_DATA_DIR = $previousDataDir
}
