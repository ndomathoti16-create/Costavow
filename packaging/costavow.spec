# PyInstaller recipe for the portable Windows desktop release.

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules


ROOT = Path(SPECPATH).resolve().parent

datas = [
    (str(ROOT / "app.py"), "."),
    (str(ROOT / ".streamlit" / "config.toml"), ".streamlit"),
    (str(ROOT / "data" / "demo"), "data/demo"),
    (str(ROOT / "docs" / "assets"), "docs/assets"),
    (str(ROOT / "PRIVACY.md"), "."),
    (str(ROOT / "SECURITY.md"), "."),
    (str(ROOT / "THIRD_PARTY_NOTICES.md"), "."),
    (str(ROOT / "THIRD_PARTY_LICENSES.txt"), "."),
]
binaries = []
hiddenimports = collect_submodules("finops_cost_intelligence")

for package in (
    "azure.identity",
    "azure.storage.blob",
    "google.cloud.bigquery",
):
    hiddenimports += collect_submodules(package)

for package in ("streamlit", "webview"):
    package_datas, package_binaries, package_hidden = collect_all(
        package, include_py_files=False, filter_submodules=lambda name: ".testing" not in name
    )
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hidden

a = Analysis(
    [str(ROOT / "desktop.py")],
    pathex=[str(ROOT / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# Keep credentials/SSO support and the exact AWS services this application exposes.
# ponytail: add a service here when a new connector needs its Botocore model.
AWS_SERVICES = {"s3", "sts", "sso", "sso-oidc", "athena", "cost-optimization-hub", "signin"}

def runtime_data(entry):
    path = Path(entry[0]).as_posix()
    if path.startswith(("pyarrow/include/", "pyarrow/tests/")):
        return False
    parts = path.split("/")
    return not (
        len(parts) > 3 and parts[:2] == ["botocore", "data"] and parts[2] not in AWS_SERVICES
    )

a.datas = [entry for entry in a.datas if runtime_data(entry)]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Costavow",
    icon=str(ROOT / "docs" / "assets" / "costavow.ico"),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
