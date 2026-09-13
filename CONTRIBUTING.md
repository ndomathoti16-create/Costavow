# Contributing and reporting issues

Start with the [developer guide](docs/DEVELOPMENT.md) for setup and required checks.

The repository has no project distribution license yet. Contact the owner before submitting
substantial external contributions or reusing the code; do not assume an open-source grant.
Third-party code or assets must have clear provenance and compatible permission, with required
notices preserved.

## Bug reports

Use the [bug report form](https://github.com/ndomathoti16-create/Costavow/issues/new/choose).
Include the version or commit, operating system, demo/desktop/source mode, reproduction steps,
and expected versus actual behavior. Use the bundled synthetic data or a minimal fictional sample.
Do not attach credentials, real billing exports, customer identifiers, or unredacted logs.

For vulnerabilities, follow [SECURITY.md](SECURITY.md). Do not publish exploit details in an issue.

## Proposed changes

Keep changes focused. Explain the user-visible behavior and the checks run. Financial or
security-sensitive changes need a regression check covering the failure case. Update metric,
privacy, or setup documentation when the corresponding behavior changes. Do not add dependencies
for functionality already covered by the standard library or existing packages.

Run the checks in the developer guide before opening a pull request. Generated local data, virtual
environments, credentials, and build outputs do not belong in a commit. Dependency update PRs
require compatibility checks; a successful dependency-bot run is not proof that application CI passed.
