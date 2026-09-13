# Changelog

Source changes on `main` are listed here before they are packaged. Downloaded release ZIPs remain
unchanged until a new version is published.

## Unreleased

### Fixed

- Require patched Setuptools for source builds and development/release verification environments.

- Correct rolling MAD anomaly scores, finite-value validation, budget currency checks, and
  selected-period business-volume comparisons.
- Refresh source caches when nested values or same-named supporting files change.
- Bound file expansion and AI responses; refuse AI redirects; sanitize parser and crash errors;
  preserve previous local state if an atomic replacement fails.
- Collect installed modern and legacy license/notice files for release review.
- Make the desktop upload smoke test follow enabled UI controls. Use the hosted runtime pin in
  CI, Docker, and desktop builds; fail release verification on the first failed check.

### Changed

- Remove unused UI renderers, obsolete sidebar CSS, unused dependencies, and duplicated helpers.
- Clarify external data sharing and prevent hosted-demo S3 actions even when S3 is configured.
- Reorganize the README, setup guide, and documentation index. Mark historical planning material
  and distinguish released screenshots from unreleased calculation changes.
- Add regression coverage for financial, ingestion, persistence, provider, and report boundaries.

Anomaly counts can differ from v0.2.3 because the prior-window MAD calculation was corrected.
No migration or new hosted customer-data service is introduced.

## [0.2.3](https://github.com/ndomathoti16-create/Metrora/releases/tag/v0.2.3) — 2026-09-08

Portable Windows release with a synthetic, read-only hosted demo; a separate local data workspace;
read-only billing connections; decision tracking; and downloadable analysis artifacts. The release
provides `Metrora-Windows-x64.zip` and `SHA256SUMS.txt`.

[Changes since v0.2.2](https://github.com/ndomathoti16-create/Metrora/compare/v0.2.2...v0.2.3).
The executable is unsigned. Review the release's source, privacy notice, and third-party notices
before using or redistributing it.
