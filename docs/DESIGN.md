# Costavow visual design

Reviewed 2026-09-13 for v0.3.0. The direction is a light analytical workspace: keep the data
legible, the next action visible, and the evidence easy to inspect. This is an original
implementation in the existing Streamlit, CSS, and Plotly stack; no design-system library,
remote font, copied component, or new service is introduced.

## Research and decisions

- [Fluent 2 color](https://fluent2.microsoft.design/color) separates neutral surfaces, brand
  emphasis, and semantic feedback. Costavow uses neutral paper and white surfaces, a restrained
  cobalt action color, and explicit status labels. Large saturated panels and decorative glow
  have been removed. Blue is a project choice, not a universal psychological guarantee of trust.
- [Material color theming](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md)
  describes named roles and foreground/background relationships. The palette is assigned by
  function across native controls, custom components, exports, and charts. We adopt the principle,
  not Material's component implementation or dynamic theme machinery.
- [Carbon color](https://carbondesignsystem.com/elements/color/overview/) uses neutral layering
  to organize working surfaces. Costavow uses white cards against a pale page, thin separators,
  compact tables, and typography to organize dense financial information.
- [Carbon chart guidance](https://carbondesignsystem.com/data-visualization/chart-types/) starts
  with the comparison the chart needs to support. Actuals use solid teal lines, forecasts use
  dashed amber lines, and anomalies use red diamonds. Legends, hover values, and detail tables
  provide additional cues. Cobalt is also used for labeled category comparisons; it does not
  denote a good or bad financial outcome.
- [WCAG text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) calls
  for 4.5:1 for normal text, or 3:1 for large text.
  [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) requires
  3:1 where visual information is necessary to identify controls or understand graphics.
  These measurements inform the palette; they are not an accessibility certification.

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

- System fonts, including Segoe UI on Windows; tabular numerals in metrics and data tables.
- A small spacing scale, 6–10 px corner radii, thin borders, and minimal shadow.
- A single light theme for the public preview, workspace, native desktop startup, and charts.
- Navigation above the work; stacked content and a two-column navigation grid on narrow screens.
- Visible keyboard focus, at least 24 px icon targets, and 44 px main button targets.
- No decorative orbit animation or scroll-reveal dependency. Content is visible immediately.
- Actual and modeled financial values remain explicitly labeled. Color never establishes savings
  verification or causal attribution.

## Verification and limits

The regression suite checks intended text, control, and action color pairs and all primary
workspace routes. Browser review covers the product, decisions, forecast chart, receipt download,
and narrow-screen overflow using synthetic data. Native Streamlit widgets retain their semantics.
A full screen-reader, high-contrast Windows, zoom, and color-vision accessibility audit remains a
human review task; automated palette checks do not cover every rendered state.
