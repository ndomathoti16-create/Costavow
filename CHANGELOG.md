# Changelog

Source changes on `main` are listed here before they are packaged. Downloaded release ZIPs remain
unchanged until a new version is published.

## [0.3.0](https://github.com/ndomathoti16-create/Costavow/releases/tag/v0.3.0) — 2026-09-13

- Ship the new `Costavow.exe` portable Windows application and matching icon.
- Replace accumulated dark theme overrides with one light workspace theme and one product
  stylesheet: paper surfaces, slate text, cobalt actions, and teal actuals.
- Distinguish forecasts with dashed amber lines and anomalies with red diamonds.
- Retain keyboard focus, readable tables, responsive layouts, and measured color-contrast guards.
- Document the Fluent, Material, Carbon, and WCAG research behind the design.

- Rebrand current source as **Costavow**, with an original vector mark and evidence-led messaging.
- Add a portable decision receipt with source references, ownership, financial basis, supplied
  actuals, and explicit interpretation limits. Synthetic demo receipts can be downloaded too.
- Do not sum measured outcomes across mixed or unknown currencies.
- Preserve legacy launch settings, local storage, and decision IDs. v0.2.3 assets are unchanged.
- Add current competitor research and a concise engineering review path.

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

## [0.2.3](https://github.com/ndomathoti16-create/Costavow/releases/tag/v0.2.3) â€” 2026-09-08

Portable Windows release with a synthetic, read-only hosted demo; a separate local data workspace;
read-only billing connections; decision tracking; and downloadable analysis artifacts. The release
provides `Metrora-Windows-x64.zip` and `SHA256SUMS.txt`.

[Changes since v0.2.2](https://github.com/ndomathoti16-create/Costavow/compare/v0.2.2...v0.2.3).
The executable is unsigned. Review the release's source, privacy notice, and third-party notices
before using or redistributing it.
