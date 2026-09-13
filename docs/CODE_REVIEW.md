# Code cleanup and boundary review

## Delivered changes

Production and packaging Python source decreased from 18,709 to 18,232 lines (477 fewer,
including the new shared state writer). Regression tests and documentation are excluded from
that comparison. No third-party implementation was copied and no new service was introduced.

- Removed four unused UI renderers and the CSS used only by the retired sidebar. Active layout,
  keyboard-focus rules, and chart styling remain in place.
- Removed unused Pydantic, pydantic-settings, and python-dotenv direct requirements. NumPy was
  already installed through the numerical stack; its existing application imports now have an
  explicit requirement. Kept Streamlit's GitPython minimum-version constraint.
- Shared numeric normalization, automatic demo/upload model preparation, and atomic JSON writes.
  Invalid state files fail visibly; failed replacement preserves the previous state file.
- Corrected rolling MAD to use a single median per prior window, retained the no-lookahead
  baseline, and preserved the sign of zero-scale anomalies. Existing demo counts can change.
- Reject non-finite financial input, conflicting budget/actual currencies, and invalid budget
  periods. Zero actual spend is distinct from no matched rows. Zero-tolerance reconciliation
  handles zero totals. Partial usage evidence no longer claims comparable usage.
- Restrict business volume to the selected billing date window and reject inconsistent units.
  Closed decisions no longer suppress priority scores for current work.
- Include nested source values and supporting-upload content in cache identities; support nested
  tag values during profiling.
- Bound optional uploads, expanded Excel/Parquet files, loaded-table memory, cloud imports, and AI
  response bytes. Refuse AI redirects, validate summary structure, and use deterministic fallback
  for invalid responses. Close S3 response bodies after reading.
- Escape report units, extend CSV formula handling, sanitize parser/crash errors, describe AI data
  sharing in the UI, and prevent hosted-demo S3 actions even if server settings enable S3.
- Fix license-file discovery for modern and legacy installed distributions. Release verification
  now stops on a failed command, and release tag text is read as data rather than interpolated into
  PowerShell source.

## Verification

- **151 tests passed**, including 38 new regression cases, existing Streamlit page/navigation
  smoke tests, and a loopback HTTP test that verifies AI redirects are refused.
- Ruff lint and formatting passed; all 107 Python files are formatted. Python compilation and
  `git diff --check` passed. Bandit reported no findings (two existing informational suppression
  warnings remain on the allow-listed BigQuery query).
- GitHub Linux CI also passed all 151 tests, lint, formatting, compilation, and Bandit. Its
  dependency audit identified the runner's preinstalled Setuptools 79.0.1; build and development
  requirements now enforce 83 or newer, the patched version in the
  [upstream advisory](https://github.com/pypa/setuptools/security/advisories/GHSA-h35f-9h28-mq5c).
- `pip check` passed. `pip-audit --local` found no known vulnerabilities in installed third-party
  packages; the local Metrora project has no PyPI advisory entry and was skipped. UTF-8 mode was
  required because the Windows workspace name contains an em dash.
- Generated a review inventory at `build/review-third-party-licenses.txt`: NumPy contributed 20
  license/notice files, pandas one, and GitPython two. The release workflow regenerates its own
  inventory from its build environment; the checked-in previous bundle was preserved.

## Security / Privacy / Licensing Review

**Measures:** input and response bounds, strict financial-value checks, HTML/CSV escaping, redirect
refusal, safer errors, atomic private temporary files, and a hosted-demo external-action boundary.

**Sensitive data:** billing values, cloud account/resource identifiers, source and service names,
owner labels, decision notes, and local profiles. Core analysis remains local. Optional AI sends
its fact pack to the configured provider; cloud refresh-on-open can repeat an earlier authorized
connection. Local data is retained until deleted. Application crash reports omit exception
messages; third-party service logs still need review before sharing.

**Dependencies and provenance:** no new external package or service was required. Existing license
notices were preserved. License inventory collection follows the installed-file locations described
in the [Python packaging metadata specification](https://packaging.python.org/en/latest/specifications/core-metadata/#license-file-multiple-use).
MAD uses the [standard median absolute deviation definition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_abs_deviation.html).

**Remaining assumptions:** this is a single-user local workspace with no tenant authentication,
application encryption, automatic retention, or multi-writer transactions. Parsing is in-process;
size checks are not an OS memory/CPU sandbox. Floating-point arithmetic, overlapping budget rows,
partial budget periods, missing metric dates, additive metric assumptions, and model uncertainty
need analyst review as described in `METRIC_DEFINITIONS.md`. AI validation cannot establish the
truth of every narrative claim.

**Human verification:** select the project's distribution license before authorizing outside reuse;
review the exact release's dependency notices and missing-license markers; approve cloud IAM,
AI-provider terms, data retention, backups, and device access/encryption. Determine any legal,
privacy, or financial-services obligations from the actual deployment and jurisdiction. Live cloud
identities, remote AI providers, the Windows executable build, and deployment were not exercised
in this review. No compliance certification or complete security guarantee is made.
