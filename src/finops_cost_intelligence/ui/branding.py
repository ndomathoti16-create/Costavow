"""Shared Costavow visual identity and Streamlit presentation helpers."""

# ruff: noqa: E501

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING

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
    --page: #f4f6f8;
    --surface: #ffffff;
    --ink: #192a3c;
    --muted: #53647a;
    --line: #d5dde7;
    --control: #788899;
    --primary: #3159d9;
    --observed: #137562;
    --warning: #946000;
    --danger: #b4233b;
}
html, body, [data-testid="stApp"] { font-family: 'Segoe UI', system-ui, sans-serif; color: var(--ink); }
[data-testid="stAppViewContainer"], [data-testid="stApp"] { background: var(--page); }
[data-testid="stHeader"] { background: var(--page); }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
.block-container { max-width: 1440px; padding: 4.5rem 3rem 4rem; }
h1, h2, h3, h4 { color: var(--ink); font-family: inherit; font-weight: 650; letter-spacing: -.025em; }
h1 { font-size: 2.1rem; } h2 { font-size: 1.6rem; } h3 { font-size: 1.15rem; }
p { line-height: 1.6; }
small, [data-testid="stCaptionContainer"] { color: var(--muted); }
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
[data-testid="stButton"] button, [data-testid="stDownloadButton"] button,
[data-testid="stLinkButton"] a {
    min-height: 2.75rem; border-radius: 6px; box-shadow: none; font-weight: 600;
}
[data-testid="stButton"] button[kind="secondary"], [data-testid="stDownloadButton"] button {
    border-color: var(--control); background: var(--surface); color: var(--ink);
}
[data-testid="stButton"] button[kind="primary"] {
    background: var(--primary); border-color: var(--primary); color: white;
}
[data-testid="stButton"] button:disabled { opacity: .55; }
[data-testid="stTextInputRootElement"], [data-baseweb="select"] > div,
[data-testid="stNumberInputContainer"], [data-testid="stTextArea"] textarea {
    background: var(--surface); border-color: var(--control); border-radius: 6px;
}
[data-testid="stFileUploaderDropzone"], [data-testid="stExpander"] {
    background: var(--surface); border: 1px solid var(--line); border-radius: 8px;
}
[data-testid="stFileUploaderDropzone"] { border: 1px dashed var(--control); }
[data-testid="stMetric"] {
    padding: 1rem 1.1rem; background: var(--surface); border: 1px solid var(--line); border-radius: 8px;
}
[data-testid="stMetricValue"] { font-size: clamp(1.5rem, 2.3vw, 2.2rem); font-variant-numeric: tabular-nums; }
[data-testid="stMetricLabel"] { color: var(--muted); }
[data-testid="stPlotlyChart"] { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
[data-baseweb="tab-list"] { gap: 1rem; border-bottom: 1px solid var(--line); }
[data-baseweb="tab"] { min-height: 2.75rem; color: var(--muted); }
[data-baseweb="tab"][aria-selected="true"] { color: var(--primary); font-weight: 700; }
.metrora-topbar, .metrora-topbar-brand, .metrora-topbar-context {
    display: flex; align-items: center; gap: .75rem;
}
.metrora-topbar { justify-content: space-between; padding: .25rem 0 1rem; border-bottom: 1px solid var(--line); }
.metrora-topbar-mark { display: flex; width: 40px; height: 40px; flex: 0 0 40px; }
.metrora-logo { width: 100%; height: 100%; }
.metrora-topbar-name { font-size: 1.15rem; font-weight: 750; letter-spacing: -.03em; }
.metrora-topbar-subtitle, .metrora-topbar-context { font-size: .75rem; color: var(--muted); }
.metrora-topbar-context i, .metrora-visual-status i { width: 7px; height: 7px; background: var(--observed); border-radius: 50%; }
.metrora-product-top-links { display: flex; justify-content: flex-end; flex-wrap: wrap; gap: .5rem; padding: .75rem 0; }
.metrora-product-top-links a { padding: .7rem .9rem; font-size: .85rem; font-weight: 600; text-decoration: none; border-radius: 6px; }
.metrora-product-top-links a:hover { background: #e8eefb; }
.metrora-product-demo-link { border: 1px solid var(--primary); }
.st-key-metrora_top_nav { margin: .7rem 0 1.5rem; }
.st-key-metrora_top_nav [data-testid="stButton"] button { font-size: .8rem; padding: .5rem .4rem; }
.st-key-metrora_top_nav [data-testid="stHorizontalBlock"] { gap: .3rem; }
.metrora-workspace-title-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: .8rem; }
.metrora-workspace-topbar { display: block; margin: .5rem 0 1rem; }
.metrora-workspace-location { display: flex; align-items: center; flex-wrap: wrap; gap: .5rem; margin-bottom: .8rem; }
.metrora-workspace-context-item { display: grid; gap: .25rem; }
.metrora-workspace-page-title { font-size: 2rem; font-weight: 700; letter-spacing: -.035em; }
.metrora-workspace-title-copy p { margin: .4rem 0; color: var(--muted); max-width: 70ch; }
.metrora-workspace-location, .metrora-workspace-command-meta, .metrora-workspace-state,
.metrora-workspace-context-item { font-size: .8rem; color: var(--muted); }
.metrora-workspace-command-meta { display: flex; gap: 1rem; flex-wrap: wrap; }
.metrora-workspace-state { padding: .35rem .6rem; border: 1px solid var(--line); border-radius: 4px; background: var(--surface); }
.metrora-panel-heading, .metrora-driver-head, .metrora-flow-heading { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; }
.metrora-panel-heading { margin: 1rem 0 .6rem; }
.metrora-panel-heading h3 { margin: 0; }
.metrora-panel-heading span, .metrora-period-context, .metrora-subsection-label { color: var(--muted); font-size: .8rem; }
.metrora-analysis-flow, .metrora-decision-snapshot, .metrora-empty-state,
.metrora-report-decision, .metrora-advanced-note { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 1.2rem; margin: .8rem 0 1.2rem; }
.metrora-flow-heading { font-size: .8rem; color: var(--muted); margin-bottom: 1rem; }
.metrora-flow-track { display: flex; align-items: center; gap: .5rem; }
.metrora-flow-node { display: grid; flex: 1; grid-template-columns: 1.5rem 1fr; gap: .2rem .5rem; min-width: 0; }
.metrora-flow-node i { grid-row: span 2; font-style: normal; font-size: .8rem; color: var(--primary); }
.metrora-flow-node span { font-size: .8rem; font-weight: 650; }
.metrora-flow-node b, .metrora-flow-node small { grid-column: 2; color: var(--muted); font-size: .75rem; font-weight: 400; }
.metrora-flow-link { width: 1.5rem; height: 1px; background: var(--line); }
.metrora-automation-note, .metrora-source-strip, .metrora-planning-strip {
    display: flex; flex-wrap: wrap; align-items: center; gap: .7rem 1.5rem; padding: 1rem 1.2rem;
    background: #edf2fc; border-left: 3px solid var(--primary); margin: 1rem 0;
}
.metrora-automation-note span, .metrora-planning-strip small, .metrora-source-strip span { color: var(--muted); font-size: .85rem; }
.metrora-planning-strip > div { display: grid; gap: .2rem; }
.metrora-planning-strip span { font-size: .75rem; color: var(--muted); }
.metrora-planning-strip strong { font-size: .85rem; }
.metrora-snapshot-lead { padding-bottom: .8rem; border-bottom: 1px solid var(--line); }
.metrora-snapshot-lead p { margin: .5rem 0; }
.metrora-snapshot-signal, .metrora-attention-item { padding: .8rem 0; border-bottom: 1px solid var(--line); }
.metrora-snapshot-signal span, .metrora-snapshot-signal small { color: var(--muted); font-size: .85rem; }
.metrora-driver-list, .metrora-governance-list, .metrora-decision-list { display: grid; gap: .75rem; margin: 1rem 0; }
.metrora-driver-row, .metrora-governance-row, .metrora-decision-row, .metrora-connection-row {
    display: grid; gap: 1rem; padding: 1.1rem; border: 1px solid var(--line); background: var(--surface); border-radius: 8px;
}
.metrora-driver-row { grid-template-columns: 3rem minmax(0, 1fr); }
.metrora-driver-head strong { color: var(--ink); }
.metrora-driver-head span, .metrora-driver-why, .metrora-driver-body p { color: var(--muted); font-size: .85rem; }
.metrora-driver-body p { margin: .4rem 0; }
.metrora-governance-row { grid-template-columns: 1fr 1.3fr 1fr; }
.metrora-governance-row > div, .metrora-connection-row > div { display: grid; gap: .35rem; }
.metrora-governance-row p { margin: 0; font-size: .85rem; }
.metrora-governance-row span { font-weight: 650; font-size: .8rem; }
.metrora-governance-row.met span { color: var(--observed); }
.metrora-governance-row.attention span { color: var(--danger); }
.metrora-connection-row { grid-template-columns: 1fr 1fr; }
.metrora-connection-row span { color: var(--primary); font-size: .8rem; }
.metrora-decision-row { grid-template-columns: 3.5rem minmax(0, 1.2fr) minmax(0, 1fr); align-items: center; }
.metrora-decision-score { display: grid; text-align: center; gap: .2rem; border-right: 1px solid var(--line); }
.metrora-decision-score span { color: var(--ink); font-size: 1.5rem; font-weight: 700; }
.metrora-decision-score small, .metrora-decision-meta small { font-size: .7rem; }
.metrora-decision-main { display: grid; gap: .4rem; min-width: 0; }
.metrora-decision-main > span { color: var(--primary); font-size: .75rem; font-weight: 650; }
.metrora-decision-main p { margin: 0; font-size: .85rem; color: var(--muted); }
.metrora-decision-meta { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .7rem; }
.metrora-decision-meta > div { display: grid; gap: .3rem; padding-left: .7rem; border-left: 1px solid var(--line); min-width: 0; }
.metrora-decision-meta strong, .metrora-decision-meta span { overflow-wrap: anywhere; font-size: .75rem; }
.metrora-decision-meta span { color: var(--muted); }
.metrora-table-shell { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); margin: .75rem 0; }
.metrora-data-table { border-collapse: collapse; width: 100%; font-size: .85rem; font-variant-numeric: tabular-nums; }
.metrora-data-table th, .metrora-data-table td { padding: .7rem .9rem; text-align: left; border-bottom: 1px solid var(--line); white-space: nowrap; }
.metrora-data-table th { background: #edf1f5; color: var(--ink); font-weight: 650; }
.metrora-data-table tr:last-child td { border-bottom: 0; }
.metrora-data-table tbody tr:hover { background: #f4f6f8; }
.metrora-report-kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 1rem 0; }
.metrora-report-kpi { display: grid; gap: .4rem; padding: 1rem; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
.metrora-report-kpi strong { font-size: 1.35rem; }
.metrora-report-kpi span, .metrora-report-kpi small { font-size: .8rem; color: var(--muted); }
.metrora-report-answers { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.metrora-report-answers > div, .metrora-report-action { padding: 1rem; border-left: 3px solid var(--primary); background: var(--surface); }
.metrora-report-priority, .metrora-section-kicker { color: var(--primary); font-size: .8rem; font-weight: 700; }
.metrora-empty-state { display: flex; gap: 1rem; padding: 2rem; }
.metrora-empty-icon { font-size: 2rem; color: var(--primary); }
.metrora-next-step { color: var(--primary); font-weight: 600; }
@media (max-width: 900px) {
    .block-container { padding: 4.5rem 1.25rem 3rem; }
    .metrora-decision-row { grid-template-columns: 3.5rem minmax(0, 1fr); }
    .metrora-decision-meta { grid-column: 1 / -1; }
    .metrora-report-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .metrora-topbar-context { max-width: 12rem; text-align: right; }
}
@media (max-width: 600px) {
    .block-container { padding: 4.5rem 1rem 2rem; }
    .metrora-topbar-context { display: none; }
    .metrora-product-top-links { justify-content: flex-start; gap: .2rem; }
    .metrora-product-top-links a { padding: .7rem .5rem; font-size: .8rem; }
    .st-key-metrora_top_nav [data-testid="stHorizontalBlock"] { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .st-key-metrora_top_nav [data-testid="stColumn"] { width: 100%; min-width: 0; }
    .metrora-workspace-title-row, .metrora-workspace-topbar { align-items: flex-start; flex-direction: column; }
    .metrora-flow-track { flex-direction: column; align-items: stretch; }
    .metrora-flow-link { display: none; }
    .metrora-flow-node { padding: .4rem 0; }
    .metrora-report-answers, .metrora-governance-row, .metrora-connection-row { grid-template-columns: 1fr; }
    .metrora-panel-heading, .metrora-driver-head { flex-wrap: wrap; gap: .4rem; }
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
        context = "Local product preview / no sign-in required"

    st.markdown(
        f"""
        <header class="metrora-topbar">
            <div class="metrora-topbar-brand">
                <span class="metrora-topbar-mark">{METRORA_LOGO_SVG}</span>
                <div>
                    <div class="metrora-topbar-name">Costavow</div>
                    <div class="metrora-topbar-subtitle">FinOps decision evidence</div>
                </div>
            </div>
            <div class="metrora-topbar-context">{context}</div>
        </header>
        """,
        unsafe_allow_html=True,
    )

    if not is_workspace:
        if st.session_state.get("product_page", "Product") == "Demo":
            st.markdown(
                """
                <nav class="metrora-product-top-links" aria-label="Product navigation">
                    <a class="metrora-product-demo-link" href="?surface=product&amp;page=Product" target="_self">Back to product</a>
                </nav>
                """,
                unsafe_allow_html=True,
            )
            return
        st.markdown(
            """
            <nav class="metrora-product-top-links" aria-label="Product sections">
                <a href="#metrora-overview">Overview</a>
                <a href="#metrora-workflow">How it works</a>
                <a href="#metrora-evidence">Trust &amp; evidence</a>
                <a class="metrora-product-demo-link" href="?surface=product&amp;page=Demo" target="_self">Explore demos</a>
            </nav>
            """,
            unsafe_allow_html=True,
        )
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": text, "family": "Segoe UI, sans-serif"},
        title_font={"color": text, "family": "Segoe UI, sans-serif"},
        legend={"font": {"color": muted}},
        hoverlabel={
            "bgcolor": PALETTE["surface"],
            "bordercolor": PALETTE["control"],
            "font": {"color": text, "family": "Segoe UI, sans-serif"},
        },
        xaxis={
            "gridcolor": grid,
            "linecolor": line,
            "tickfont": {"color": muted},
            "title_font": {"color": muted},
            "automargin": True,
            "zeroline": False,
        },
        yaxis={
            "gridcolor": grid,
            "linecolor": line,
            "tickfont": {"color": muted},
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
    st.markdown(
        f'<div class="metrora-table-shell">{table_html}</div>',
        unsafe_allow_html=True,
    )
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
