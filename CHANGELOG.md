# Changelog

Source changes on `main` are listed here before they are packaged. Downloaded release ZIPs remain
unchanged until a new version is published.

## [0.4.0](https://github.com/ndomathoti16-create/Costavow/releases/tag/v0.4.0) — 2026-09-14

- Replace the website-like workspace navigation with a persistent native sidebar, compact page
  headers, restrained styling, and working Ctrl+Alt+number navigation shortcuts.
- Bring the overview chart and attention queue forward; expand driver evidence on demand.
- Make the decision queue searchable and let desktop users select a row to review it.
- Open the synthetic sample directly on first run and put report exports before the preview.
- Calculate only the selected planning/decision panel and generate export files on download.
- Package Windows as one executable to avoid the reproduced .NET failure on Internet-marked
  loose runtime DLLs. Verify marked-download native startup and normal shutdown in release CI.
- Remove duplicated Python data files, unused AWS service models, and PyArrow development
  headers/test data from the Windows package. Preserve supported connectors and license notices.
- Keep validation, hosted-demo restrictions, calculations, local storage paths, and saved decisions.

## [0.3.1](https://github.com/ndomathoti16-create/Costavow/releases/tag/v0.3.1) — 2026-09-14

- Move the public project website to GitHub Pages with original responsive HTML/CSS, editorial
  typography, clear section spacing, real desktop/mobile demo previews, and native keyboard-accessible FAQs.
- Focus the Streamlit entry on three synthetic scenarios; update the current demo address to
  `costavow.streamlit.app` and remove the repeated marketing layouts.
- Fix overlapping driver rows in Overview and Reports, run-together labels, report answer cards,
  decision metadata, metric wrapping, and mobile chart legend/axis collisions.
- Render escaped component HTML directly, retain the logo, and improve readability across the
  shared web/desktop workspace. Keep secondary validation details available on demand.
- Add real-browser regressions at six viewport widths. Publish the website only after Python and
  browser checks pass; use Node 24 actions throughout.
- Preserve existing financial calculations, hosted-demo boundaries, and legacy local data paths.

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

## [0.2.3](https://github.com/ndomathoti16-create/Costavow/releases/tag/v0.2.3) — 2026-09-08

Portable Windows release with a synthetic, read-only hosted demo; a separate local data workspace;
read-only billing connections; decision tracking; and downloadable analysis artifacts. The release
provides `Metrora-Windows-x64.zip` and `SHA256SUMS.txt`.

[Changes since v0.2.2](https://github.com/ndomathoti16-create/Costavow/compare/v0.2.2...v0.2.3).
The executable is unsigned. Review the release's source, privacy notice, and third-party notices
before using or redistributing it.
