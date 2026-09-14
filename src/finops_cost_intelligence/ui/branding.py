"""Shared Costavow visual identity and Streamlit presentation helpers."""

# ruff: noqa: E501

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..config import Settings


PRODUCT_NAME = "Costavow"
PRODUCT_SUBTITLE = "FinOps decision evidence"
PRODUCT_DESCRIPTION = (
    "Every cost claim needs a trail. Reconcile the evidence, own the decision, review the outcome."
)

METRORA_LOGO_SVG = """
<svg class="metrora-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="Costavow logo">
  <rect x="1" y="1" width="46" height="46" rx="8" fill="#3159D9"/>
  <path d="M32 11H18a7 7 0 0 0-7 7v12a7 7 0 0 0 7 7h14" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M20 19h10M20 25h8M20 31h10" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
  <path d="m36 19 5 5-5 5-5-5z" fill="#FFFFFF"/>
</svg>
"""


PALETTE = {
    "page": "#f4f6f8",
    "surface": "#ffffff",
    "ink": "#192a3c",
    "muted": "#53647a",
    "line": "#d5dde7",
    "control": "#788899",
    "primary": "#3159d9",
    "observed": "#137562",
    "warning": "#946000",
    "danger": "#b4233b",
}


WORKSPACE_CSS = """
<style>
:root {
    color-scheme: light;
    --page: #f4f6f8; --surface: #ffffff; --ink: #192a3c; --muted: #53647a;
    --line: #d5dde7; --control: #788899; --primary: #3159d9;
    --observed: #137562; --warning: #946000; --danger: #b4233b;
}
html, body, [data-testid="stApp"] { font-family: 'Segoe UI', system-ui, sans-serif; color: var(--ink); }
[data-testid="stAppViewContainer"], [data-testid="stApp"], [data-testid="stHeader"] { background: var(--page); }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
.block-container { max-width: 1280px; padding: 4.5rem 2.5rem 5rem; }
h1, h2, h3, h4 { color: var(--ink); font-weight: 650; letter-spacing: -.025em; }
p { line-height: 1.65; }
small, [data-testid="stCaptionContainer"] { color: var(--muted); font-size: .875rem; line-height: 1.6; }
a { color: var(--primary); text-underline-offset: .2em; }
button, input, select, textarea { font: inherit; }
:where(button, a, input, textarea, select, [tabindex]):focus-visible {
    outline: 3px solid var(--primary) !important; outline-offset: 3px !important;
}
[data-testid="stHeaderActionElements"] a,
[data-testid="stPlotlyChart"] .modebar-btn,
[data-testid="stTabsScrollRight"], [data-testid="stTabsScrollLeft"] {
    min-width: 1.5rem; min-height: 1.5rem;
}
[data-testid="stButton"] button, [data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {
    min-height: 2.875rem; border-radius: 9px; padding: .65rem 1rem; box-shadow: none; font-weight: 600;
}
[data-testid="stButton"] button[kind="secondary"], [data-testid="stDownloadButton"] button {
    border-color: var(--control); background: var(--surface); color: var(--ink);
}
[data-testid="stButton"] button[kind="primary"] { background: var(--primary); border-color: var(--primary); color: white; }
[data-testid="stButton"] button:disabled { opacity: .55; }
[data-testid="stTextInputRootElement"], [data-baseweb="select"] > div,
[data-testid="stNumberInputContainer"], [data-testid="stTextArea"] textarea {
    background: var(--surface); border-color: var(--control); border-radius: 8px;
}
[data-testid="stFileUploaderDropzone"], [data-testid="stExpander"], [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
}
[data-testid="stFileUploaderDropzone"] { border: 1px dashed var(--control); }
[data-testid="stMetric"] { height: 100%; padding: 1.5rem; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
[data-testid="stMetricValue"] { font-size: clamp(1.4rem, 2.15vw, 2rem); font-variant-numeric: tabular-nums; }
[data-testid="stMetricLabel"] { color: var(--muted); }
.st-key-workspace-kpi-strip [data-testid="stHorizontalBlock"] { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
.st-key-workspace-kpi-strip [data-testid="stColumn"] { width: 100%; min-width: 0; }
[data-testid="stPlotlyChart"] { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
[data-baseweb="tab-list"] { gap: 1.25rem; border-bottom: 1px solid var(--line); }
[data-baseweb="tab"] { min-height: 3rem; color: var(--muted); }
[data-baseweb="tab"][aria-selected="true"] { color: var(--primary); font-weight: 700; }
.metrora-topbar, .metrora-topbar-brand, .metrora-topbar-context { display: flex; align-items: center; gap: .875rem; }
.metrora-topbar { justify-content: space-between; padding: .25rem 0 1.25rem; border-bottom: 1px solid var(--line); }
.metrora-topbar-mark { display: flex; width: 42px; height: 42px; flex: 0 0 42px; }
.metrora-logo { width: 100%; height: 100%; }
.metrora-topbar-name { font-size: 1.375rem; font-weight: 750; letter-spacing: -.04em; }
.metrora-topbar-subtitle, .metrora-topbar-context { font-size: .875rem; color: var(--muted); }
.metrora-topbar-context { max-width: 50%; text-align: right; }
.metrora-topbar-context i { width: 8px; height: 8px; background: var(--observed); border-radius: 50%; flex-shrink: 0; }
.metrora-product-top-links { display: flex; justify-content: flex-end; flex-wrap: wrap; gap: 1.5rem; }
.metrora-product-top-links a { display: inline-flex; align-items: center; min-height: 44px; font-size: .9375rem; text-decoration: none; }
.metrora-product-top-links a:hover { text-decoration: underline; }
.st-key-metrora_top_nav { margin: .25rem 0 1.5rem; }
.st-key-metrora_top_nav [data-testid="stHorizontalBlock"] { display: flex; flex-wrap: wrap; gap: .375rem; }
.st-key-metrora_top_nav [data-testid="stColumn"] { flex: 1 0 auto; width: auto; min-width: 0; }
.st-key-metrora_top_nav [data-testid="stButton"] button { padding: .65rem .75rem; }
.st-key-metrora_top_nav [data-testid="stButton"] button p { font-size: .9375rem; white-space: nowrap; }
.metrora-workspace-topbar { margin: .5rem 0 1.5rem; }
.metrora-workspace-location { display: flex; align-items: center; flex-wrap: wrap; gap: .65rem; margin-bottom: 1.25rem; font-size: .875rem; color: var(--muted); }
.metrora-workspace-state { padding: .25rem .6rem; border: 1px solid var(--line); border-radius: 6px; background: var(--surface); }
.metrora-workspace-title-row { display: grid; grid-template-columns: minmax(0, 1fr) 340px; align-items: center; gap: 2.5rem; }
.metrora-workspace-page-title { font-size: clamp(1.8rem, 3vw, 2.5rem); line-height: 1.2; font-weight: 650; letter-spacing: -.04em; }
.metrora-workspace-title-copy p { margin: .75rem 0 0; color: var(--muted); max-width: 72ch; }
.metrora-workspace-command-meta { display: flex; flex-wrap: wrap; gap: .75rem 1.5rem; padding-left: 1.5rem; border-left: 1px solid var(--line); }
.metrora-workspace-context-item { display: grid; gap: .25rem; min-width: 0; }
.metrora-workspace-context-item strong { font-size: .9375rem; font-weight: 600; overflow-wrap: anywhere; }
.metrora-panel-heading { display: flex; justify-content: space-between; flex-wrap: wrap; align-items: baseline; gap: .5rem 1rem; margin: 1rem 0 .75rem; }
.metrora-panel-heading > span { font-size: 1.125rem; font-weight: 650; }
.metrora-panel-heading h3 { margin: 0; }
.metrora-period-context { display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; color: var(--muted); font-size: .875rem; margin: .5rem 0 1.5rem; }
.metrora-period-context strong { color: var(--ink); }
.metrora-section-kicker, .metrora-subsection-label { color: var(--primary); font-size: .875rem; font-weight: 650; letter-spacing: .06em; }
.metrora-analysis-flow, .metrora-decision-snapshot, .metrora-empty-state, .metrora-report-decision,
.metrora-advanced-note { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem; margin: .25rem 0 1.5rem; }
.metrora-flow-heading { display: flex; justify-content: space-between; gap: 1rem; font-size: .9375rem; color: var(--muted); margin-bottom: 1.25rem; }
.metrora-flow-track { display: flex; align-items: center; gap: 1rem; }
.metrora-flow-node { display: flex; align-items: flex-start; flex: 1; gap: .75rem; min-width: 0; }
.metrora-flow-node > span { color: var(--primary); font-size: .875rem; padding-top: .1rem; }
.metrora-flow-node > div { display: grid; gap: .25rem; }
.metrora-flow-node strong { font-size: .9375rem; }
.metrora-flow-link { width: 1rem; height: 1px; background: var(--line); }
.metrora-automation-note, .metrora-planning-strip, .metrora-source-strip {
    display: flex; flex-wrap: wrap; align-items: start; gap: 1rem 2rem; padding: 1.5rem;
    background: #edf2fc; border-left: 3px solid var(--primary); border-radius: 0 10px 10px 0; margin: 1rem 0 1.5rem;
}
.metrora-automation-note { display: grid; gap: .5rem; }
.metrora-automation-note span, .metrora-advanced-note span { display: block; color: var(--muted); line-height: 1.65; }
.metrora-source-strip > div, .metrora-planning-strip > div { display: grid; gap: .375rem; min-width: 0; }
.metrora-source-strip strong { overflow-wrap: anywhere; }
.metrora-planning-strip span { font-size: .875rem; color: var(--muted); }
.metrora-decision-snapshot { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.5rem; }
.metrora-snapshot-lead { grid-column: 1 / -1; padding-bottom: 1.5rem; border-bottom: 1px solid var(--line); }
.metrora-snapshot-lead > span, .metrora-snapshot-signal > span { display: block; font-size: .875rem; color: var(--muted); margin-bottom: .5rem; }
.metrora-snapshot-lead > strong { display: block; font-size: 1.5rem; letter-spacing: -.025em; }
.metrora-snapshot-signal > strong { display: block; font-size: 1.125rem; }
.metrora-snapshot-lead p, .metrora-snapshot-signal p { margin: .5rem 0 0; color: var(--muted); font-size: .9375rem; }
.metrora-attention-item { padding: 1.25rem 0; border-top: 1px solid var(--line); }
.metrora-attention-item p { margin: .5rem 0 0; color: var(--muted); font-size: .9375rem; }
.metrora-driver-list, .metrora-governance-list, .metrora-decision-list { display: grid; gap: 1.25rem; margin: 1rem 0 2rem; }
.metrora-driver-row, .metrora-governance-row, .metrora-decision-row, .metrora-connection-row {
    display: grid; gap: 1.5rem; padding: 1.75rem; border: 1px solid var(--line); background: var(--surface); border-radius: 12px;
}
.metrora-driver-row { grid-template-columns: minmax(0, 1fr); }
.metrora-driver-head { display: flex; justify-content: space-between; flex-wrap: wrap; align-items: start; gap: 1rem; }
.metrora-driver-head > div { display: grid; gap: .4rem; }
.metrora-driver-head strong, .metrora-driver-head b { font-size: 1.125rem; }
.metrora-driver-head span { color: var(--muted); font-size: .9375rem; }
.metrora-driver-body { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.25rem 2rem; border-top: 1px solid var(--line); padding-top: 1.25rem; }
.metrora-driver-body > div { display: grid; align-content: start; gap: .375rem; min-width: 0; }
.metrora-driver-why { grid-column: 1 / -1; }
.metrora-driver-body p { margin: 0; color: var(--muted); font-size: .9375rem; max-width: 90ch; }
.metrora-driver-body strong { font-size: .9375rem; font-weight: 600; overflow-wrap: anywhere; }
.metrora-governance-row { grid-template-columns: 1fr 1.4fr 1.3fr; align-items: start; }
.metrora-governance-row > div, .metrora-connection-row > div { display: grid; gap: .5rem; }
.metrora-governance-row p { margin: 0; font-size: .9375rem; }
.metrora-governance-row span { font-weight: 650; font-size: .875rem; }
.metrora-governance-row.met span { color: var(--observed); }
.metrora-governance-row.attention span { color: var(--danger); }
.metrora-connection-row { grid-template-columns: 1fr 1fr; }
.metrora-connection-row span { color: var(--primary); font-size: .875rem; }
.metrora-decision-row { grid-template-columns: 4rem minmax(0, 1fr); align-items: start; }
.metrora-decision-score { display: grid; text-align: center; gap: .25rem; padding: .75rem .25rem; background: var(--page); border-radius: 8px; }
.metrora-decision-score span { font-size: 1.75rem; font-weight: 650; }
.metrora-decision-score small { font-size: .875rem; }
.metrora-decision-main { display: grid; gap: .625rem; min-width: 0; }
.metrora-decision-main > span { color: var(--primary); font-size: .875rem; }
.metrora-decision-main > strong { font-size: 1.125rem; }
.metrora-decision-main p { margin: 0; font-size: .9375rem; color: var(--muted); max-width: 85ch; }
.metrora-decision-meta { grid-column: 2; display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--line); }
.metrora-decision-meta > div { display: grid; align-content: start; gap: .375rem; min-width: 0; }
.metrora-decision-meta strong, .metrora-decision-meta span { overflow-wrap: anywhere; font-size: .9375rem; }
.metrora-decision-meta span { color: var(--muted); }
.metrora-table-shell { overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); margin: 1rem 0; }
.metrora-data-table { border-collapse: collapse; width: 100%; font-size: .9375rem; font-variant-numeric: tabular-nums; }
.metrora-data-table th, .metrora-data-table td { padding: 1rem; text-align: left; border-bottom: 1px solid var(--line); white-space: nowrap; }
.metrora-data-table th { background: #edf1f5; font-weight: 650; }
.metrora-data-table tr:last-child td { border-bottom: 0; }
.metrora-data-table tbody tr:hover { background: var(--page); }
.metrora-report-kpis { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.metrora-report-kpi { display: grid; align-content: start; gap: .625rem; padding: 1.5rem; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); }
.metrora-report-kpi strong { font-size: 1.6rem; }
.metrora-report-kpi span { font-size: .9375rem; color: var(--muted); }
.metrora-report-answers { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.5rem; margin: 1.5rem 0; }
.metrora-report-answers > article, .metrora-report-action { padding: 1.5rem; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); }
.metrora-report-answers > article p { margin: .75rem 0 0; }
.metrora-report-action { display: grid; gap: 1rem; margin: 1rem 0; }
.metrora-report-action small { display: block; margin-top: .5rem; }
.metrora-report-priority { color: var(--primary); font-size: .875rem; font-weight: 650; }
.metrora-report-decision h2 { margin: .75rem 0; font-size: 1.75rem; }
.metrora-report-decision p { color: var(--muted); margin-bottom: 0; }
.metrora-empty-state { display: flex; align-items: start; gap: 1.5rem; padding: 2rem; }
.metrora-empty-icon { font-size: 2rem; color: var(--primary); }
.metrora-next-step { color: var(--primary); font-weight: 600; }
.costavow-demo-intro { max-width: 760px; margin: 3rem auto; text-align: center; }
.costavow-demo-intro h1 { font-family: Georgia, serif; font-weight: 400; font-size: clamp(2.75rem, 5vw, 4.5rem); line-height: 1.1; margin: 1rem 0 1.5rem; }
.costavow-demo-intro p { font-size: 1.125rem; color: var(--muted); max-width: 60ch; margin: auto; }
.st-key-demo-scenarios [data-testid="stHorizontalBlock"] { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.5rem; }
.st-key-demo-scenarios [data-testid="stColumn"] { width: 100%; min-width: 0; }
.st-key-demo-scenarios [class*="st-key-scenario-"] { padding: 1.5rem; background: var(--surface); border-color: var(--line); border-radius: 12px; }
.costavow-scenario { min-height: 19rem; }
.costavow-scenario h2 { font-size: 1.5rem; line-height: 1.25; margin: 1.25rem 0; }
.costavow-scenario p { font-size: 1rem; color: var(--muted); }
.costavow-scenario-lesson { border-top: 1px solid var(--line); padding-top: 1rem; }
.costavow-demo-boundary { max-width: 760px; margin: 3rem auto 0; padding-top: 2rem; border-top: 1px solid var(--line); text-align: center; }
.costavow-demo-boundary p { color: var(--muted); }
.costavow-demo-boundary a { display: inline-flex; min-height: 44px; align-items: center; }
@media (max-width: 1100px) {
    .block-container { padding-inline: 1.5rem; }
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) > [data-testid="stColumn"] { width: 100%; min-width: 0; }
    .costavow-scenario { min-height: 23rem; }
}
@media (max-width: 900px) {
    .metrora-workspace-title-row { grid-template-columns: 1fr; gap: 1.25rem; }
    .metrora-workspace-command-meta { border-left: 0; border-top: 1px solid var(--line); padding: 1rem 0 0; }
    [data-testid="stHorizontalBlock"]:has(.st-key-home-trend-surface),
    .st-key-demo-scenarios [data-testid="stHorizontalBlock"] { flex-direction: column; grid-template-columns: 1fr; }
    [data-testid="stHorizontalBlock"]:has(.st-key-home-trend-surface) > [data-testid="stColumn"],
    .st-key-demo-scenarios [data-testid="stColumn"] { width: 100%; }
    .metrora-flow-track { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    .metrora-flow-link { display: none; }
    .metrora-report-answers { grid-template-columns: 1fr; }
    .costavow-scenario { min-height: 0; }
}
@media (max-width: 600px) {
    .block-container { padding: 4.5rem 1rem 3rem; }
    .metrora-topbar-context { display: none; }
    .metrora-topbar-subtitle { font-size: .875rem; }
    .metrora-product-top-links { justify-content: start; gap: 1rem; }
    .st-key-metrora_top_nav [data-testid="stHorizontalBlock"] { display: grid; grid-template-columns: 1fr 1fr; }
    .st-key-metrora_top_nav [data-testid="stColumn"] { width: 100%; }
    .st-key-metrora_top_nav [data-testid="stButton"] button { padding-inline: .5rem; }
    .metrora-decision-snapshot, .metrora-driver-body, .metrora-governance-row,
    .metrora-connection-row, .metrora-report-kpis { grid-template-columns: 1fr; }
    .metrora-driver-row, .metrora-decision-row { padding: 1.25rem; gap: 1.25rem; }
    .metrora-decision-row { grid-template-columns: 3.5rem minmax(0, 1fr); }
    .metrora-decision-meta { grid-column: 1 / -1; grid-template-columns: 1fr; gap: 1.25rem; }
    .metrora-driver-head strong, .metrora-driver-head b { overflow-wrap: anywhere; }
    .metrora-analysis-flow { padding: 1.25rem; }
    [data-testid="stMetric"] { padding: 1rem; }
    [data-testid="stMetricValue"] { font-size: 1.4rem; }
    .costavow-demo-intro { margin: 2rem 0; text-align: left; }
    .costavow-demo-boundary { text-align: left; }
    .st-key-demo-scenarios [class*="st-key-scenario-"] { padding: 1.25rem; }
}
@media (max-width: 380px) {
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) { grid-template-columns: 1fr; }
    .metrora-flow-track { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; } }
</style>
"""


def inject_styles() -> None:
    """Apply the shared light theme to product and workspace surfaces."""
    import streamlit as st

    st.html(WORKSPACE_CSS)


def render_top_navigation(settings: Settings) -> None:
    """Render the full-width navigation shared by product and workspace views."""
    import streamlit as st

    from .navigation import set_product_route, set_workspace_route

    is_workspace = bool(st.session_state.get("demo_authenticated", False))
    has_source = st.session_state.get("loaded_table") is not None
    has_model = st.session_state.get("normalized_table") is not None
    report = st.session_state.get("quality_report")
    analysis_ready = bool(has_model and report is not None and report.ready_for_analysis)

    if is_workspace:
        workspace_label = st.session_state.get(
            "demo_workspace", f"{settings.app_env.title()} workspace"
        )
        status_label = "Analysis ready" if analysis_ready else "Review needed"
        context = f"<i></i>{escape(str(workspace_label))} / {status_label}"
    else:
        context = "Interactive demo / synthetic data"

    st.html(f"""
        <header class="metrora-topbar">
            <div class="metrora-topbar-brand">
                <span class="metrora-topbar-mark"><img class="metrora-logo" alt="" src="data:image/svg+xml,{quote(METRORA_LOGO_SVG)}"></span>
                <div>
                    <div class="metrora-topbar-name">Costavow</div>
                    <div class="metrora-topbar-subtitle">FinOps decision evidence</div>
                </div>
            </div>
            <div class="metrora-topbar-context">{context}</div>
        </header>
        """)

    if not is_workspace:
        st.html("""
            <nav class="metrora-product-top-links" aria-label="Project links">
                <a href="https://ndomathoti16-create.github.io/Costavow/" target="_top">Product website ↗</a>
                <a href="https://github.com/ndomathoti16-create/Costavow" target="_blank" rel="noopener noreferrer">View the code ↗</a>
            </nav>
        """)
        return

    desktop_mode = bool(st.session_state.get("desktop_mode", False))
    pages = [
        ("Overview", "Home", "home"),
        ("Explore spend", "Cost explorer", "cost_explorer"),
        ("Forecast & alerts", "Plans & alerts", "plans_alerts"),
        ("Decisions", "Decisions", "decisions"),
        ("Reports & exports", "Reports", "reports"),
        ("Data settings", "Advanced", "advanced"),
    ]
    if desktop_mode:
        pages.insert(5, ("Data sources", "Connections", "connections"))
    legacy_pages = {
        "Overview": "Home",
        "Spend explorer": "Cost explorer",
        "Forecast & alerts": "Plans & alerts",
        "Reports & exports": "Reports",
        "Data sources": "Connections",
        "Data settings": "Advanced",
        "Data & quality": "Advanced",
        "Investigate": "Plans & alerts",
    }
    current_page = legacy_pages.get(
        st.session_state.get("workspace_page", "Home"),
        st.session_state.get("workspace_page", "Home"),
    )
    st.session_state["workspace_page"] = current_page

    with st.container(key="metrora_top_nav"):
        action_count = 1
        weights = [1] * (len(pages) + action_count)
        columns = st.columns(weights, gap="small")
        for column, (label, destination, slug) in zip(columns[: len(pages)], pages, strict=True):
            with column:
                if st.button(
                    label,
                    key=f"top_workspace_nav_{slug}",
                    type="primary" if destination == current_page else "tertiary",
                    width="stretch",
                ):
                    set_workspace_route(destination)
                    st.rerun()
        with columns[-1]:
            if desktop_mode:
                if st.button(
                    "New analysis",
                    key="top_workspace_new_analysis",
                    disabled=not (has_source or has_model),
                    width="stretch",
                    help="Clear the current data and start a new analysis.",
                ):
                    reset_workspace_state()
                    for key in ("demo_mode", "demo_scenario", "demo_workspace"):
                        st.session_state.pop(key, None)
                    set_workspace_route("Home", scenario_id=None)
                    st.rerun()
            else:
                if st.button(
                    "Exit demo",
                    key="top_workspace_back_to_product",
                    width="stretch",
                    help="Return to the Costavow demo scenarios.",
                ):
                    reset_workspace_state()
                    for key in (
                        "demo_authenticated",
                        "demo_mode",
                        "demo_scenario",
                        "demo_user_email",
                        "demo_workspace",
                    ):
                        st.session_state.pop(key, None)
                    set_product_route("Demo")
                    st.rerun()


def apply_plotly_theme(figure):
    """Apply Costavow's light chart palette."""
    text = PALETTE["ink"]
    muted = PALETTE["muted"]
    grid = PALETTE["line"]
    line = PALETTE["line"]
    figure.update_layout(
        margin={"l": 64, "r": 36, "t": 72, "b": 112},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": text, "family": "Segoe UI, sans-serif", "size": 14},
        title={
            "x": 0.04,
            "xanchor": "left",
            "font": {"color": text, "family": "Segoe UI, sans-serif", "size": 16},
        },
        legend={
            "font": {"color": muted, "size": 13},
            "orientation": "h",
            "y": 0.02,
            "x": 0.04,
            "yref": "container",
            "xref": "container",
            "yanchor": "bottom",
            "title_text": None,
        },
        hoverlabel={
            "bgcolor": PALETTE["surface"],
            "bordercolor": PALETTE["control"],
            "font": {"color": text, "family": "Segoe UI, sans-serif"},
        },
        xaxis={
            "gridcolor": grid,
            "linecolor": line,
            "tickfont": {"color": muted, "size": 12},
            "title_font": {"color": muted},
            "automargin": True,
            "zeroline": False,
        },
        yaxis={
            "gridcolor": grid,
            "linecolor": line,
            "tickfont": {"color": muted, "size": 12},
            "title_font": {"color": muted},
            "automargin": True,
            "zeroline": False,
        },
    )
    return figure


def render_compact_table(dataframe, *, max_rows: int = 20) -> None:
    """Render a bounded, theme-safe HTML table for operational detail views."""
    import streamlit as st

    if dataframe.empty:
        st.info("No rows are available for this view.")
        return
    bounded = dataframe.head(max_rows)
    table_html = bounded.to_html(
        index=False,
        border=0,
        classes="metrora-data-table",
        escape=True,
        na_rep="-",
    )
    st.html(f'<div class="metrora-table-shell">{table_html}</div>')
    if len(dataframe) > max_rows:
        st.caption(f"Showing the first {max_rows:,} of {len(dataframe):,} rows.")


def reset_workspace_state() -> None:
    """Clear data and widget state while preserving app preferences."""
    import streamlit as st

    exact_keys = {
        "loaded_table",
        "data_profile",
        "column_mapping",
        "normalized_table",
        "normalized_source_key",
        "mapping_source_key",
        "quality_report",
        "quality_source_key",
        "warehouse_summary",
        "warehouse_source_key",
        "fact_pack",
        "summary_result",
        "decision_register",
        "analytics_filtered_table",
        "analytics_source_key",
        "budget_table",
        "budget_upload_key",
        "business_metrics_table",
        "business_upload_key",
        "workspace_page",
        "auto_attempted_source_key",
        "auto_analysis_message",
        "auto_analysis_error",
        "mapping_edit_mode",
        "summary_source_key",
        "billing_upload",
    }
    prefixes = (
        "mapping_",
        "analysis_",
        "breakdown_",
        "forecast_",
        "anomaly_",
        "allocation_",
        "business_metric_",
        "budget_",
        "business_upload_",
        "s3_upload_",
        "summary_button_",
        "download_",
    )
    for key in list(st.session_state):
        if key in exact_keys or key.startswith(prefixes):
            st.session_state.pop(key, None)
