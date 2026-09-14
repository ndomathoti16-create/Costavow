# Costavow visual design

Reviewed 2026-09-14 for v0.4.0. The public site uses an editorial product layout; the analytical
workspace uses the same slate, cobalt, and neutral roles with a more functional type hierarchy.
This revision fixes measured component failures rather than adding another layer of theme overrides.

## Reference study and original direction

- [Kairo](https://getkairo.xyz/) gives a single message room to lead, separates sections clearly,
  and presents a short numbered process. Costavow adopts the spacing and hierarchy principles.
  Its security claims, content, assets, animations, and dark visual identity are not reused.
- [Cluely](https://cluely.com/) pairs a large serif headline with a prominent product demonstration
  and focused supporting sections. Costavow uses a system serif for public display headings,
  a real synthetic workspace capture, and native expandable answers. No competitor imagery,
  source code, testimonials, metrics, or logos are copied.
- [Fluent color roles](https://fluent2.microsoft.design/color) and
  [Carbon color](https://carbondesignsystem.com/elements/color/overview/) inform neutral working
  surfaces and restrained semantic accents. Color is assigned by function; blue is not a claim
  of psychological trust. [WCAG contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
  and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
  inform legibility and control cues.

The public page has one primary demo action, a Windows download, three workflow steps, the
portable receipt distinction, inspectable engineering choices, and a short FAQ. Repeated process
maps, generic evidence bars, and overlapping product explanations were removed. The receipt
schematic is explicitly labeled as an illustration; financial screenshots use the bundled synthetic data.

## Root causes repaired

| Observed problem | Repair |
| --- | --- |
| Driver heading constrained to 48 pixels, overlapping the explanation and amount | Full-width heading followed by a separate evidence grid; shared by Overview and Reports. |
| Labels and values ran together in source strips, flow nodes, and snapshots | Explicit block/grid relationships matching the actual child tags. |
| Report answers lacked card spacing | Style the actual `article` children. |
| Metadata squeezed beside decision descriptions | Move metadata to its own row; stack fields on small screens. |
| Markdown rewrote custom HTML headings and children | Use sanitized `st.html` with existing escaping and JavaScript disabled; embed the logo as an image. |
| Four metrics wrapped into an accidental three-plus-one layout | A deliberate grid with responsive breakpoints. |
| Chart legends crossed mobile axis labels | Use Plotly's native container-referenced legend positioning and automatic margin growth. |
| Dense setup detail displaced the primary overview | Keep source/model workflow available in an expander below the analysis. |

## Palette and measured contrast

White surfaces are `#FFFFFF`; the page is `#F4F6F8`. Ratios use the WCAG sRGB luminance formula.
Values below are rounded for display; the regression check compares unrounded values.

| Role | Color | Against white | Against page |
| --- | --- | --- | --- |
| ink | `#192A3C` | 14.61:1 | 13.48:1 |
| muted | `#53647A` | 6.05:1 | 5.58:1 |
| primary | `#3159D9` | 5.90:1 | 5.44:1 |
| observed | `#137562` | 5.60:1 | 5.17:1 |
| warning | `#946000` | 5.34:1 | 4.93:1 |
| danger | `#B4233B` | 6.47:1 | 5.98:1 |
| control | `#788899` | 3.63:1 | 3.35:1 |

Ink and muted text support the information hierarchy. Cobalt marks actions, selected navigation,
and keyboard focus. Teal marks observed data and labeled successful checks. Amber marks modeled
forecasts and caution; red marks anomalies or errors. Control borders use the stronger neutral;
`#D5DDE7` is a decorative separator, not the only cue that identifies an input.
White button text on cobalt uses the same contrast ratio as cobalt on white.

## Layout and interaction

The static site has a 1200-pixel content ceiling, 100-pixel desktop section spacing, 64-pixel mobile
section spacing, 16–19-pixel body copy, and large Georgia display headings. Native links, anchors,
and `details` work without scripts. Visible focus, skip navigation, reduced-motion behavior, and
at least 44-pixel primary targets are included. Dedicated mobile screenshots avoid shrinking a
whole desktop dashboard into an unreadable phone image.

The workspace has a 1280-pixel outer ceiling, 14–16-pixel supporting text, generous row padding,
and one shared component stylesheet. The palette remains consistent with desktop and exports.
Forecast actuals use solid teal; estimates use dashed amber; bounds are dotted; anomalies have
red diamond markers. Labels and line styles carry meaning in addition to color.

## Hosting decision

The public project website is ordinary HTML/CSS on GitHub Pages. It requires no Python session,
client JavaScript, remote fonts, analytics, cookies, or build framework. Its metadata and responsive
layout are independent of Streamlit's application shell. Pages is appropriate for this independent
project showcase; it is not selected as a commercial SaaS host. See
[GitHub's usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

[Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) can
also host these exact static files and remains a straightforward future move if a separate hosting
account or domain workflow is needed. It provides no immediate product benefit that requires an
additional account for this release. A full frontend/API rewrite would duplicate a functioning
Python analytical workflow and expand authentication and data-handling scope. Streamlit therefore
remains the synthetic interactive demo and local desktop UI, with its actual layout defects repaired.

## Verification and limits

`tests/browser_check.cjs` checks six viewport widths and every main workspace page, plus planning
tabs, the HTML receipt download, keyboard entry, image loading, and actual component geometry.
Python AppTests retain route restoration, quality blockers, financial boundaries, and hosted-demo
restrictions. Automated checks complement visual inspection; passing checks are not an accessibility
certification. Browser rendering and system fonts vary by operating system. Custom Streamlit selectors
must be checked again when upgrading the framework. The hosted demo can still have Community Cloud
startup delays; the public static website does not depend on that session.


## Application design review — v0.4.0

The desktop workspace is an operating tool. A persistent native sidebar replaces the wide site-like
navigation; a 24px page title and a compact source/status line replace the repeated hero. The first
screen prioritizes cost metrics, the trend, and actions. The separate GitHub Pages site retains its
editorial presentation. These changes use the existing Streamlit/WebView2 stack, without a new
frontend framework, command-palette dependency, remote font, animation library, or backend service.

| Reference, reviewed from its publisher | Principle applied to Costavow |
| --- | --- |
| [Linear: calmer interface](https://linear.app/now/behind-the-latest-design-refresh) | Receding navigation, consistent headers, and lower visual weight for supporting information. |
| [Things: Quick Find](https://culturedcode.com/things/blog/2019/12/the-quick-find-update/) | Direct navigation and a focused decision search, with a stable place for each task. |
| [Craft: styling](https://support.craft.do/hc/en-us/articles/10293992410780-Document-Styling) | Clear document hierarchy in reports; editorial display styling stays on the public site. |
| [Raycast: action panel](https://manual.raycast.com/action-panel) | Discoverable actions next to their context, and keyboard access without an extra menu system. |
| [Superhuman: shortcuts](https://help.superhuman.com/hc/en-us/articles/46005789591693-Speed-Up-With-Shortcuts) | Working navigation shortcuts, with a visible reminder; ordinary typing remains unaffected. |
| [Stripe: dashboard basics](https://docs.stripe.com/dashboard/basics) | Persistent navigation, data grids, explicit scope, and exports placed before the report preview. |
| [Notion: sidebar](https://www.notion.com/help/navigate-with-the-sidebar) | Grouped destinations, native collapse/resize, and reusable interface primitives. |
| [Airbnb: visual language](https://medium.com/airbnb-design/building-a-visual-language-behind-the-scenes-of-our-airbnb-design-system-224748775e4e) | Consistent components, approachable labels, and restrained spacing. |
| [Duolingo: shape language](https://blog.duolingo.com/shape-language-duolingos-art-style/) | A recognizable accent and simple shapes. Financial work does not benefit from mascots or gamification. |
| [Arc: command actions](https://start.arc.net/command-bar-actions) | Reach the intended action directly. Six or seven destinations do not require a custom command palette. |

The implementation is original. References inform principles; no competitor code, assets, icons,
trademarks, or proprietary interface were copied. Icons use the existing Streamlit Material set.
Control transitions last 120ms and respect reduced-motion preferences. Evidence uses native
`details` elements; collapsed evidence is available through mouse, touch, and keyboard.

The decision queue uses a searchable native grid. In the desktop app, selecting a row opens its
existing review form; saved decisions and their evidence remain in the same local store. Starting a
new analysis explicitly describes the session reset. First-run users can load the bundled synthetic
sample directly instead of downloading and re-uploading it.

### Measured optimization and limits

Three warm AppTest reruns per page with the same 236-row synthetic source on the same Windows
machine gave these medians before and after the initial layout/performance changes:

| Page | Before | After | Structural change |
| --- | --- | --- | --- |
| Overview | 135ms | 114ms | Remove the repeated snapshot and redundant input copy. |
| Forecast & alerts | 205ms | 80ms | Render the active tab: 1 chart / 3 metrics instead of 4 charts / 16 metrics. |
| Reports | 132ms | 112ms | Serialize export files on download instead of each page render. |

These are local synthetic-data script timings, not production latency or large-data guarantees.
Browser resizing, keyboard navigation, all planning tabs, exports, and a hidden-panel regression
check validate behavior. No global cache of user financial data was introduced. Deferred exports
use [Streamlit's native download callback](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button),
and lazy panels use [stateful tabs](https://docs.streamlit.io/develop/api-reference/layout/st.tabs).
Large numerical libraries remain because the app actually uses them for forecasting and file support.
There is no claim that every operation or dependency is universally optimal.

### Windows download-origin failure

Windows can preserve an Internet-origin mark on DLLs extracted from a downloaded ZIP.
An isolated marked copy of the released `Python.Runtime.dll` reproduced the reported failure in
`clr_loader.netfx._get_callable`; the same unmarked copy resolved successfully. Microsoft documents
this [.NET Framework assembly-loading behavior](https://learn.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/runtime/loadfromremotesources-element).
The earlier automated extraction check did not preserve the mark and therefore missed the failure.

The release now uses PyInstaller's standard single-executable packaging. Runtime libraries are
embedded and expanded into a per-run temporary folder, instead of being distributed as loose DLLs
for Explorer to mark. The executable retains its download-origin mark; no application code removes
Windows trust metadata, changes machine security policy, or grants remote assemblies full trust.
The release workflow launches a marked executable through CreateProcess and verifies that its
native window opens and closes normally. It tests runtime startup after launch, not the Explorer
SmartScreen/publisher confirmation. License texts are also included as readable files beside the executable.

Single-file startup includes decompression and can be slower than a folder build. Do not run it as
administrator; it uses the current user's permissions. Temporary execution may be prohibited by
organizational application-control policy. PyInstaller documents these
[packaging tradeoffs](https://pyinstaller.org/en/stable/operating-mode.html#bundling-to-one-file).
The binary remains unsigned; signing needs a verified publisher identity and signing service.
