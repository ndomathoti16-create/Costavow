"""Public Costavow product pages and local-only demo access flow."""

# ruff: noqa: E501

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

from ..contracts.normalization import NormalizedTable
from ..contracts.profile import DataProfile
from ..contracts.quality import QualityReport
from ..ingestion import IngestionError, LoadedTable, load_table, profile_table
from ..mapping import MappingValidationError
from ..normalization.budgets import normalize_budget_dataframe
from ..normalization.business_metrics import normalize_business_metrics
from ..runtime import resource_path
from .branding import reset_workspace_state
from .mapping_view import build_automatic_model, source_key_for
from .navigation import set_product_route, set_workspace_route

if TYPE_CHECKING:
    from ..config import Settings


PUBLIC_PAGES = ("Product", "Demo")

DEFAULT_DEMO_SCENARIO = "forecast_risk"
DEMO_SCENARIOS: dict[str, dict[str, str]] = {
    "healthy": {
        "label": "Healthy baseline",
        "status": "Ready to share",
        "description": "Clean, stable spend with complete ownership and comfortable budget headroom.",
        "lesson": "See what a low-risk, decision-ready review looks like.",
        "billing": "cloud_billing_healthy.csv",
        "budget": "budget_healthy.csv",
        "business": "business_metrics_healthy.csv",
    },
    "quality_risk": {
        "label": "Data needs review",
        "status": "Blocked on quality",
        "description": "Mixed currency, invalid required values, duplicates, and ownership gaps.",
        "lesson": "See how Costavow stops unreliable numbers before analysis.",
        "billing": "cloud_billing_quality_risk.csv",
        "budget": "budget_quality_risk.csv",
        "business": "business_metrics_quality_risk.csv",
    },
    "forecast_risk": {
        "label": "Hidden future risk",
        "status": "Healthy now, watch next",
        "description": "Reconciled spend that is currently controlled but accelerating into the forecast.",
        "lesson": "See why a clean current period can still require action.",
        "billing": "cloud_billing_demo.csv",
        "budget": "budget_demo.csv",
        "business": "business_metrics_demo.csv",
    },
}


PRODUCT_PAGE_CSS = """
<style>
.metrora-product-hero { display: grid; grid-template-columns: 1.05fr 1fr; gap: 3rem; align-items: center; padding: 3rem 0 2rem; }
.metrora-product-kicker, .metrora-product-section-kicker, .metrora-native-bridge header > span,
.metrora-live-connections header > span { color: var(--primary); font-size: .75rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.metrora-hero-copy h1 { position: relative; padding: 0; font-size: clamp(2.6rem, 4.5vw, 4.25rem); line-height: 1.08; letter-spacing: -.05em; margin: 1rem 0 1.3rem; }
.metrora-hero-copy h1 > span:first-child > span, .metrora-hero-copy h1 em { display: block; }
.metrora-hero-copy h1 [data-testid="stHeaderActionElements"] { position: absolute; right: 0; bottom: 0; line-height: 1; }
.metrora-hero-copy h1 em { color: var(--primary); font-style: normal; }
.metrora-hero-copy p { color: var(--muted); font-size: 1.05rem; max-width: 46ch; }
.metrora-product-pills { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.2rem; }
.metrora-product-pill { border: 1px solid var(--line); border-radius: 4px; padding: .35rem .6rem; background: var(--surface); font-size: .75rem; color: var(--muted); }
.metrora-command-surface { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 1.5rem; box-shadow: 0 8px 24px #192a3c08; }
.metrora-visual-header, .metrora-visual-footer { display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem; font-size: .75rem; color: var(--muted); }
.metrora-visual-status { display: inline-flex; align-items: center; gap: .4rem; color: var(--observed); }
.metrora-visual-metric { font-size: clamp(1.8rem, 3vw, 2.7rem); font-weight: 700; letter-spacing: -.03em; margin: 1.4rem 0; font-variant-numeric: tabular-nums; }
.metrora-visual-metric small { display: block; font-size: .8rem; font-weight: 400; letter-spacing: 0; }
.metrora-line-visual { height: 135px; border-bottom: 1px solid var(--line); margin-bottom: .8rem; }
.metrora-line-visual svg { width: 100%; height: 100%; overflow: visible; }
.metrora-chart-area { fill: url(#metrora-area); }
.metrora-chart-trace { fill: none; stroke: var(--observed); stroke-width: 3; vector-effect: non-scaling-stroke; }
.metrora-command-flow { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: .7rem; border-top: 1px solid var(--line); margin-top: 1.3rem; padding-top: 1rem; }
.metrora-command-node { display: grid; gap: .3rem; }
.metrora-command-node i { font-style: normal; color: var(--primary); font-size: .7rem; }
.metrora-command-node span { font-size: .8rem; font-weight: 650; }
.metrora-command-node b { font-weight: 400; color: var(--muted); font-size: .7rem; overflow-wrap: anywhere; }
.metrora-command-link { display: none; }
.metrora-hero-secondary-link { display: flex; justify-content: center; align-items: center; min-height: 2.75rem; padding: .4rem .7rem; border: 1px solid var(--control); border-radius: 6px; background: var(--surface); font-size: .9rem; font-weight: 600; text-decoration: none; }
.metrora-centered-caption { text-align: center; font-size: .75rem; color: var(--muted); margin: .8rem 0 2rem; }
.metrora-product-section { padding: 3.5rem 0 1rem; border-top: 1px solid var(--line); margin-top: 2rem; }
.metrora-product-section h2, .metrora-native-bridge h2, .metrora-live-connections h2 { font-size: clamp(1.6rem, 2.5vw, 2.2rem); max-width: 30ch; margin: .6rem 0 .8rem; }
.metrora-product-section p, .metrora-native-bridge header p, .metrora-live-connections header p { color: var(--muted); max-width: 80ch; }
.metrora-model-map { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); margin: 1rem 0; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
.metrora-model-node { padding: 1.2rem; border-right: 1px solid var(--line); }
.metrora-model-node:last-child { border-right: 0; }
.metrora-model-node small { display: block; font-size: .7rem; color: var(--primary); margin-bottom: .7rem; }
.metrora-model-node strong { font-size: .95rem; }
.metrora-model-node p { color: var(--muted); font-size: .8rem; margin: .5rem 0 0; }
.metrora-native-bridge, .metrora-live-connections { padding: 2rem 0; border-top: 1px solid var(--line); }
.metrora-connection-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.metrora-connection-grid article, .metrora-native-lane, .metrora-product-card, .metrora-product-principle,
.metrora-product-output, .metrora-scenario-card, .metrora-product-story, .metrora-evidence-visual {
    padding: 1.4rem; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); height: 100%;
}
.metrora-connection-grid small, .metrora-native-lane small, .metrora-product-card .icon,
.metrora-product-principle .icon, .metrora-output-mark, .metrora-scenario-card small { color: var(--primary); font-size: .75rem; font-weight: 650; }
.metrora-connection-grid h3, .metrora-native-lane h3, .metrora-product-card h3,
.metrora-product-principle h3, .metrora-product-output h3, .metrora-scenario-card h3 { margin: .7rem 0; font-size: 1.1rem; }
.metrora-connection-grid p, .metrora-native-lane li, .metrora-product-card p,
.metrora-product-principle p, .metrora-product-output p, .metrora-scenario-card p, .metrora-product-story p { color: var(--muted); font-size: .85rem; margin-bottom: 0; }
.metrora-native-lanes { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0; }
.metrora-native-lane ul { padding-left: 1.1rem; margin-bottom: 0; }
.metrora-native-lane li { margin-bottom: .5rem; }
.metrora-connection-footnote { display: grid; gap: .4rem; font-size: .8rem; color: var(--muted); }
.metrora-accountability-loop { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; border-block: 1px solid var(--line); padding: 1rem 0; }
.metrora-accountability-loop span { color: var(--primary); margin-right: .6rem; font-size: .75rem; }
.metrora-accountability-loop strong { font-size: .85rem; }
.metrora-story-list { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
.metrora-story-list span { color: var(--muted); font-size: .75rem; border: 1px solid var(--line); padding: .3rem .5rem; border-radius: 4px; }
.metrora-evidence-title { display: flex; justify-content: space-between; gap: .7rem; font-weight: 650; font-size: .9rem; }
.metrora-evidence-title b { color: var(--observed); font-size: .75rem; }
.metrora-evidence-row { margin-top: 1rem; font-size: .8rem; color: var(--muted); }
.metrora-evidence-row i { display: block; background: var(--observed); height: 6px; margin-top: .4rem; border-radius: 2px; }
.metrora-evidence-visual p { color: var(--muted); font-size: .8rem; margin: 1rem 0 0; }
.metrora-product-step { display: grid; grid-template-columns: 3rem 1fr; gap: 1rem; padding: 1.2rem 0; border-bottom: 1px solid var(--line); }
.metrora-product-step-number { color: var(--primary); font-variant-numeric: tabular-nums; }
.metrora-product-step p { margin: .25rem 0 0; color: var(--muted); font-size: .9rem; }
.metrora-centered-section { margin: 2rem 0 .7rem; }
.metrora-centered-section p { color: var(--muted); }
.metrora-product-split, .metrora-access-note { margin-top: 1.5rem; padding: 1.5rem; background: #edf2fc; border-left: 3px solid var(--primary); }
.metrora-product-split p, .metrora-access-note { color: var(--muted); font-size: .85rem; }
.metrora-product-access { margin: 1rem 0 1.5rem; }
.metrora-product-access p { color: var(--muted); }
.metrora-scenario-card { min-height: 17rem; margin-bottom: .8rem; }
.metrora-scenario-card > span { display: block; margin-top: 1rem; font-size: .8rem; color: var(--ink); }
.metrora-product-footer { border-top: 1px solid var(--line); padding: 1.5rem 0 0; margin-top: 3rem; font-size: .75rem; color: var(--muted); }
@media (max-width: 1000px) {
    .metrora-product-hero { gap: 1.5rem; }
    .metrora-model-map { grid-template-columns: 1fr; }
    .metrora-model-node { border-right: 0; border-bottom: 1px solid var(--line); }
    .metrora-model-node:last-child { border-bottom: 0; }
    .metrora-connection-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 700px) {
    .metrora-product-hero, .metrora-native-lanes, .metrora-connection-grid { grid-template-columns: 1fr; }
    .metrora-product-hero { padding-top: 1.5rem; }
    .metrora-hero-copy h1 { position: relative; padding: 0; font-size: 2.8rem; }
    .metrora-command-surface { padding: 1.1rem; }
    .metrora-product-section { padding-top: 2rem; }
    .metrora-scenario-card { min-height: 0; }
}
</style>
"""


def _demo_scenario(scenario_id: str) -> dict[str, str]:
    """Return validated metadata for one guided scenario."""
    scenario = DEMO_SCENARIOS.get(scenario_id)
    if scenario is None:
        allowed = ", ".join(DEMO_SCENARIOS)
        raise IngestionError(f"Unknown demo scenario {scenario_id!r}; choose one of: {allowed}.")
    return scenario


def _demo_path(scenario_id: str = DEFAULT_DEMO_SCENARIO) -> Path:
    scenario = _demo_scenario(scenario_id)
    return _demo_supporting_path(scenario["billing"])


def _demo_supporting_path(filename: str) -> Path:
    """Return one of the checked-in supporting files used by the guided demo."""
    return resource_path("data", "demo", filename)


def _load_demo_planning_context(settings: Settings, scenario_id: str):
    """Load normalized budget and business context for a complete guided demo."""
    scenario = _demo_scenario(scenario_id)
    budget_path = _demo_supporting_path(scenario["budget"])
    business_path = _demo_supporting_path(scenario["business"])
    missing = [path.name for path in (budget_path, business_path) if not path.is_file()]
    if missing:
        raise IngestionError("The demo support file(s) are missing: " + ", ".join(missing))
    try:
        budget = normalize_budget_dataframe(
            load_table(budget_path, max_bytes=settings.max_upload_mb * 1024 * 1024).dataframe
        )
        business_metrics = normalize_business_metrics(
            load_table(business_path, max_bytes=settings.max_upload_mb * 1024 * 1024).dataframe
        )
    except (IngestionError, ValueError) as exc:
        raise IngestionError(f"The demo planning context could not be prepared: {exc}") from exc
    return budget, business_metrics


def _set_product_page(page: str) -> None:
    """Store the selected public product page for the next Streamlit rerun."""
    if page in PUBLIC_PAGES:
        set_product_route(page)


def build_demo_artifacts(
    settings: Settings,
    scenario_id: str = DEFAULT_DEMO_SCENARIO,
) -> tuple[
    LoadedTable,
    DataProfile,
    dict[str, str | None],
    NormalizedTable,
    QualityReport,
]:
    """Load and prepare one deterministic billing scenario for a guided session."""
    demo_path = _demo_path(scenario_id)
    if not demo_path.is_file():
        raise IngestionError(
            "The demo billing file is missing. Run data/demo/generate_demo_data.py first."
        )

    loaded_table = load_table(
        demo_path,
        max_bytes=settings.max_upload_mb * 1024 * 1024,
    )
    profile = profile_table(loaded_table)
    try:
        accepted_mapping, normalized, report = build_automatic_model(loaded_table, profile)
    except (MappingValidationError, ValueError, KeyError) as exc:
        raise IngestionError(f"The demo billing file could not be prepared: {exc}") from exc

    return loaded_table, profile, accepted_mapping, normalized, report


def activate_demo_session(
    settings: Settings,
    scenario_id: str = DEFAULT_DEMO_SCENARIO,
    *,
    persist_route: bool = True,
) -> None:
    """Start a local guided demo with real Costavow analysis state."""
    scenario = _demo_scenario(scenario_id)
    loaded_table, profile, accepted_mapping, normalized, report = build_demo_artifacts(
        settings,
        scenario_id,
    )
    budget, business_metrics = _load_demo_planning_context(settings, scenario_id)
    reset_workspace_state()
    source_key = source_key_for(loaded_table, profile)
    st.session_state.update(
        {
            "demo_authenticated": True,
            "demo_mode": True,
            "demo_scenario": scenario_id,
            "demo_user_email": "demo@metrora.local",
            "demo_workspace": f"Costavow / {scenario['label']}",
            "loaded_table": loaded_table,
            "data_profile": profile,
            "mapping_source_key": source_key,
            "column_mapping": accepted_mapping,
            "normalized_table": normalized,
            "normalized_source_key": source_key,
            "quality_report": report,
            "quality_source_key": source_key,
            "budget_table": budget,
            "budget_upload_key": f"demo:{scenario['budget']}",
            "business_metrics_table": business_metrics,
            "business_upload_key": f"demo:{scenario['business']}",
            "auto_attempted_source_key": source_key,
            "workspace_page": "Home" if report.ready_for_analysis else "Advanced",
            "auto_analysis_message": (
                "Guided scenario ready. Costavow mapped, normalized, and checked the source "
                "automatically."
                if report.ready_for_analysis
                else "Costavow stopped the analysis because the guided source contains "
                "blocking quality issues. Review the highlighted checks before using its totals."
            ),
        }
    )
    if persist_route:
        set_workspace_route(
            "Home" if report.ready_for_analysis else "Advanced",
            scenario_id=scenario_id,
        )


def _demo_preview_facts(settings: Settings) -> dict[str, object]:
    """Calculate the public demo visual from the checked-in synthetic source."""
    cache_key = "_metrora_product_demo_facts"
    cached = st.session_state.get(cache_key)
    if isinstance(cached, dict):
        return cached

    loaded, profile, _, normalized, report = build_demo_artifacts(settings)
    dataframe = normalized.dataframe.copy()
    total = float(dataframe["cost"].sum())
    currencies = dataframe["currency"].dropna().astype(str).unique().tolist()
    currency = currencies[0] if len(currencies) == 1 else "Mixed"
    total_label = f"${total:,.0f}" if currency == "USD" else f"{currency} {total:,.0f}"

    daily = dataframe.groupby("usage_date", as_index=False)["cost"].sum().sort_values("usage_date")
    values = daily["cost"].astype(float).tolist()
    minimum = min(values)
    span = max(max(values) - minimum, 1.0)
    width, top, bottom = 530.0, 24.0, 150.0
    points: list[str] = []
    for index, value in enumerate(values):
        x = width * index / max(len(values) - 1, 1)
        y = bottom - ((value - minimum) / span) * (bottom - top)
        points.append(f"{x:.1f} {y:.1f}")
    chart_path = "M" + " L".join(points)
    area_path = f"{chart_path} L{width:.1f} 176 L0 176 Z"

    services = (
        dataframe.groupby("service", as_index=False)["cost"]
        .sum()
        .sort_values("cost", ascending=False)
    )
    lead_service = str(services.iloc[0]["service"])
    lead_share = float(services.iloc[0]["cost"]) / total if total else 0.0
    difference = report.reconciliation.absolute_difference or 0.0
    facts: dict[str, object] = {
        "source": loaded.source_name,
        "rows": profile.row_count,
        "total": total_label,
        "currency": currency,
        "lead_service": lead_service,
        "lead_share": lead_share,
        "difference": difference,
        "chart_path": chart_path,
        "area_path": area_path,
        "date_start": str(daily["usage_date"].min().date()),
        "date_end": str(daily["usage_date"].max().date()),
    }
    st.session_state[cache_key] = facts
    return facts


def _render_page_intro(
    kicker: str,
    title: str,
    copy: str,
    *,
    anchor_id: str | None = None,
) -> None:
    st.markdown(
        f"""
        <section{f' id="{anchor_id}"' if anchor_id else ""} class="metrora-product-section metrora-scroll-reveal">
            <div class="metrora-product-section-kicker">{kicker}</div>
            <h2>{title}</h2>
            <p>{copy}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_model_map() -> None:
    """Show the calculation-to-explanation model in a compact visual map."""
    st.markdown(
        """
        <div class="metrora-model-map metrora-scroll-reveal" role="list" aria-label="Costavow operating model">
            <div class="metrora-model-node" role="listitem">
                <small>01 / Source</small>
                <strong>Billing export</strong>
                <p>Provider rows, budgets, ownership, and business metrics.</p>
            </div>
            <div class="metrora-model-node" role="listitem">
                <small>02 / Model</small>
                <strong>Trusted cost model</strong>
                <p>Mapped, normalized, reconciled, and quality-checked data.</p>
            </div>
            <div class="metrora-model-node" role="listitem">
                <small>03 / Insight</small>
                <strong>Decision signals</strong>
                <p>Trends, drivers, forecasts, anomalies, and coverage.</p>
            </div>
            <div class="metrora-model-node" role="listitem">
                <small>04 / Action</small>
                <strong>Owned decision</strong>
                <p>Owner, due date, disposition, and evidence in one operating record.</p>
            </div>
            <div class="metrora-model-node" role="listitem">
                <small>05 / Outcome</small>
                <strong>Reviewed outcome</strong>
                <p>Compare supplied actuals, with the evidence and caveats attached.</p>
            </div>
        </div>
        <p class="metrora-centered-caption metrora-model-caption">
            Calculated first. Explained second. Traceable throughout.
        </p>
        """,
        unsafe_allow_html=True,
    )


def _render_native_bridge() -> None:
    """Explain why Costavow complements provider-native cost products."""
    st.markdown(
        """
        <section class="metrora-native-bridge metrora-scroll-reveal">
            <header>
                <span>Designed to complement the cloud</span>
                <h2>Make the finance-to-engineering handoff inspectable.</h2>
                <p>AWS, Azure, and Google Cloud remain the best source for provider-specific
                billing and resource recommendations. Costavow gives finance and engineering a
                local place to reconcile exports, record the human decision, and review
                supplied actuals with the evidence and caveats attached.</p>
            </header>
            <div class="metrora-native-lanes">
                <article class="metrora-native-lane">
                    <small>Native cloud platforms</small>
                    <h3>Provider depth</h3>
                    <ul>
                        <li>Detailed billing and resource telemetry</li>
                        <li>Provider-specific optimization recommendations</li>
                        <li>Commitment, rightsizing, and service expertise</li>
                    </ul>
                </article>
                <article class="metrora-native-lane metrora">
                    <small>Costavow decision layer</small>
                    <h3>Cross-provider accountability</h3>
                    <ul>
                        <li>Reconciled evidence and one provider-neutral cost model</li>
                        <li>Budget, ownership, and business-unit context</li>
                        <li>A portable decision receipt with ownership, evidence, actuals, and caveats</li>
                    </ul>
                </article>
            </div>
            <div class="metrora-accountability-loop" aria-label="Decision accountability loop">
                <div><span>01</span><strong>Detect</strong></div>
                <div><span>02</span><strong>Prove</strong></div>
                <div><span>03</span><strong>Assign</strong></div>
                <div><span>04</span><strong>Verify</strong></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_overview(settings: Settings) -> None:
    facts = _demo_preview_facts(settings)
    st.markdown(
        f"""
        <section id="metrora-overview" class="metrora-product-hero metrora-premium-hero">
            <div class="metrora-hero-copy">
                <div class="metrora-product-kicker">Costavow / FinOps decision evidence</div>
                <h1><span>Every cost claim</span> <em>needs a trail.</em></h1>
                <p>
                    Reconcile the billing. Record the decision. Review what changed.
                    A local FinOps workspace with a portable receipt for the evidence behind each action.
                </p>
                <div class="metrora-product-pills">
                    <span class="metrora-product-pill">One-click guided analysis</span>
                    <span class="metrora-product-pill">Evidence before AI</span>
                </div>
            </div>
            <div class="metrora-hero-visual metrora-command-surface">
                <div class="metrora-visual-header">
                    <span>Guided workspace / live sample</span>
                    <span class="metrora-visual-status"><i></i> Model ready</span>
                </div>
                <div class="metrora-visual-metric">{facts["total"]}
                    <small>{facts["rows"]:,} reconciled rows</small>
                </div>
                <div class="metrora-visual-chart metrora-line-visual" aria-label="Calculated synthetic-demo spend trend">
                    <svg viewBox="0 0 530 176" preserveAspectRatio="none" aria-hidden="true">
                        <defs>
                            <linearGradient id="metrora-area" x1="0" x2="0" y1="0" y2="1">
                                <stop offset="0" stop-color="#137562" stop-opacity=".30" />
                                <stop offset="1" stop-color="#137562" stop-opacity="0" />
                            </linearGradient>
                        </defs>
                        <path class="metrora-chart-area" d="{facts["area_path"]}" />
                        <path class="metrora-chart-trace" d="{facts["chart_path"]}" />
                    </svg>
                </div>
                <div class="metrora-visual-footer">
                    <span>Largest service driver</span>
                    <strong>{escape(str(facts["lead_service"]))} / {facts["lead_share"]:.0%} of spend</strong>
                </div>
                <div class="metrora-command-flow" aria-label="Costavow analysis flow">
                    <div class="metrora-command-node is-ready"><i>01</i><span>Source</span><b>{escape(str(facts["source"]))}</b></div>
                    <div class="metrora-command-link"><span></span></div>
                    <div class="metrora-command-node is-ready"><i>02</i><span>Model</span><b>{escape(str(facts["currency"]))} {float(facts["difference"]):,.2f} difference</b></div>
                    <div class="metrora-command-link"><span></span></div>
                    <div class="metrora-command-node is-ready is-current"><i>03</i><span>Decision</span><b>Review {escape(str(facts["lead_service"]))}</b></div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    button_columns = st.columns([1, 1.05, 1.05, 1], gap="small")
    with button_columns[1]:
        st.button(
            "Explore demo scenarios",
            type="primary",
            width="stretch",
            key="product_demo_hero",
            on_click=_set_product_page,
            args=("Demo",),
        )
    with button_columns[2]:
        st.markdown(
            '<a class="metrora-hero-secondary-link" '
            'href="https://github.com/ndomathoti16-create/Costavow/releases/latest" '
            'target="_blank" rel="noopener">Download for Windows</a>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<p class="metrora-centered-caption">'
        f"Hosted preview: {facts['rows']:,} synthetic billing rows. "
        "Costavow for Windows opens a local workspace for your own exports."
        "</p>",
        unsafe_allow_html=True,
    )

    _render_page_intro(
        "A visible operating loop",
        "From export to action, without losing the evidence.",
        "Costavow automates the normal path, keeps the workflow legible, and opens the technical "
        "detail only when a reviewer needs it.",
    )
    _render_model_map()
    st.markdown(
        """
        <section class="metrora-live-connections metrora-scroll-reveal" id="metrora-connections">
            <header>
                <span>Live cost data</span>
                <h2>Connect the exports you already schedule.</h2>
                <p>The desktop workspace imports the newest complete provider export, then
                applies the same mapping, reconciliation, quality, and decision pipeline used
                for every file.</p>
            </header>
            <div class="metrora-connection-grid" role="list" aria-label="Supported cost data sources">
                <article role="listitem"><small>01 / AWS</small><h3>Data Exports &amp; CUR</h3>
                <p>Read the latest complete CSV.GZ or Parquet batch from an S3 prefix through
                AWS SSO or an IAM role.</p></article>
                <article role="listitem"><small>02 / Azure</small><h3>Cost Management</h3>
                <p>Refresh recurring ActualCost or AmortizedCost exports from Blob Storage
                through Entra ID.</p></article>
                <article role="listitem"><small>03 / Google Cloud</small><h3>Cloud Billing</h3>
                <p>Query a BigQuery billing export with Application Default Credentials and
                include credits in effective cost.</p></article>
                <article role="listitem"><small>04 / Portable</small><h3>Files &amp; FOCUS</h3>
                <p>Open CSV, Excel, Parquet, or FOCUS-shaped exports from other cloud and
                technology providers.</p></article>
            </div>
            <p class="metrora-connection-footnote">
                <strong>Read-only by design</strong>
                <span>Costavow stores export locations and refresh history&mdash;not passwords,
                access keys, tokens, or cloud resource controls.</span>
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    _render_native_bridge()
    principles = [
        (
            "01",
            "Start with the signal",
            "See the position, movement, outlook, and exceptions that should be reviewed now.",
        ),
        (
            "02",
            "Keep the proof attached",
            "Mappings, quality checks, reconciliation, and source context remain one click away.",
        ),
        (
            "03",
            "Move the next decision forward",
            "Connect budgets and business metrics to forecasts, anomalies, and a concise brief.",
        ),
    ]
    columns = st.columns(3, gap="large")
    for column, (number, title, copy) in zip(columns, principles, strict=True):
        with column:
            st.markdown(
                f"""
                <div class="metrora-product-principle">
                    <span class="icon">{number}</span>
                    <h3>{title}</h3>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(
            """
            <div class="metrora-product-story">
                <div class="metrora-product-section-kicker">Designed for the handoff</div>
                <h3>A decision should travel with its evidence.</h3>
                <p>Finance, engineering, and FinOps teams see the same source-backed story -
                including the data caveats that change how confidently to act.</p>
                <div class="metrora-story-list">
                    <span>Mapped source fields</span><span>Reconciled totals</span>
                    <span>Visible caveats</span><span>Named next move</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="metrora-evidence-visual" aria-label="Evidence visual">
                <div class="metrora-evidence-title"><span>Decision evidence</span><b>Complete</b></div>
                <div class="metrora-evidence-row"><span>Spend movement</span><i style="width: 86%"></i></div>
                <div class="metrora-evidence-row"><span>Ownership coverage</span><i style="width: 72%"></i></div>
                <div class="metrora-evidence-row"><span>Budget context</span><i style="width: 58%"></i></div>
                <div class="metrora-evidence-row"><span>Business metric</span><i style="width: 42%"></i></div>
                <p>Every finding keeps its supporting inputs visible.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_pipeline() -> None:
    _render_page_intro(
        "The pipeline",
        "One defensible path from raw export to recommendation.",
        "Each stage turns uncertainty into a clear next action while keeping financial "
        "calculations deterministic.",
        anchor_id="metrora-workflow",
    )
    steps = [
        (
            "01",
            "Ingest",
            "Upload CSV, Excel, or Parquet and profile its shape, types, nulls, and duplicates.",
        ),
        (
            "02",
            "Map",
            "Review Costavow's column suggestions and correct the semantic fields that matter.",
        ),
        (
            "03",
            "Validate",
            "Normalize to a canonical model, reconcile source totals, and surface quality caveats.",
        ),
        (
            "04",
            "Explore",
            "Slice spend by service, account, department, project, environment, and region.",
        ),
        (
            "05",
            "Decide",
            "Forecast, investigate anomalies, connect business metrics, and export the brief.",
        ),
        (
            "06",
            "Verify",
            "Assign the owner, record the disposition, and measure the result against actuals.",
        ),
    ]
    for number, title, copy in steps:
        st.markdown(
            f"""
            <div class="metrora-product-step">
                <div class="metrora-product-step-number">{number}</div>
                <div><strong>{title}</strong><p>{copy}</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="metrora-centered-section">
            <h3>What the workflow produces</h3>
            <p>
                Each output gives the next team a clearer answer without losing the source context.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    outputs = [
        (
            "A",
            "Trusted cost model",
            "Normalized billing rows with mapping decisions, quality flags, and "
            "reconciliation context.",
        ),
        (
            "B",
            "Decision-ready analysis",
            "Trends, drivers, forecasts, anomalies, allocation coverage, and budget comparisons.",
        ),
        (
            "C",
            "Evidence-backed brief",
            "A concise explanation of what changed, why it matters, and what to investigate next.",
        ),
        (
            "D",
            "Decision record",
            "An accountable owner, disposition, due date, and actual verified outcome.",
        ),
    ]
    output_columns = st.columns(len(outputs), gap="large")
    for column, (mark, title, copy) in zip(output_columns, outputs, strict=True):
        with column:
            st.markdown(
                f"""
                <div class="metrora-product-output">
                    <span class="metrora-output-mark">{mark}</span>
                    <h3>{title}</h3>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_trust() -> None:
    _render_page_intro(
        "Trust by design",
        "Numbers first. Narrative second.",
        "Every value is calculated and checked before Costavow explains what it means.",
        anchor_id="metrora-evidence",
    )
    columns = st.columns(3, gap="medium")
    trust_cards = [
        (
            "01",
            "Deterministic calculations",
            "Financial values are computed by the analytical pipeline first. AI receives "
            "the results and supporting evidence only.",
        ),
        (
            "02",
            "Visible caveats",
            "Missing fields, duplicates, invalid values, and reconciliation differences "
            "remain visible instead of being hidden in a summary.",
        ),
        (
            "03",
            "Read-only access",
            "Cloud exports and native AWS recommendations are imported through least-privilege "
            "identities; Costavow does not change resources.",
        ),
    ]
    for column, (number, title, copy) in zip(columns, trust_cards, strict=True):
        with column:
            st.markdown(
                f"""
                <div class="metrora-product-card">
                    <span class="icon">{number}</span>
                    <h3>{title}</h3>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="metrora-product-split">
            <h3>Provider depth, neutral accountability</h3>
            <p>
                Use AWS, Azure, and Google Cloud for their native telemetry and optimization
                engines. Use Costavow to reconcile the cost story, connect it to business context,
                record what people decided, and verify the outcome from actual billing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_access_panel(settings: Settings) -> None:
    st.markdown(
        """
        <div class="metrora-product-access">
            <h3>Choose the story you want to test</h3>
            <p>
                Each scenario opens the complete workspace with its billing, budget, and
                business context already connected.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    columns = st.columns(len(DEMO_SCENARIOS), gap="large")
    for column, (scenario_id, scenario) in zip(
        columns,
        DEMO_SCENARIOS.items(),
        strict=True,
    ):
        with column:
            st.markdown(
                f"""
                <article class="metrora-scenario-card">
                    <small>{escape(scenario["status"])}</small>
                    <h3>{escape(scenario["label"])}</h3>
                    <p>{escape(scenario["description"])}</p>
                    <span>{escape(scenario["lesson"])}</span>
                </article>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Open {scenario['label'].lower()}",
                type="secondary",
                width="stretch",
                key=f"product_demo_scenario_{scenario_id}",
            ):
                try:
                    activate_demo_session(settings, scenario_id)
                except IngestionError as exc:
                    st.error(str(exc))
                else:
                    st.rerun()
    st.markdown(
        """
        <div class="metrora-access-note">
            <strong>Read-only product demo.</strong>
            Every scenario is synthetic and deterministic. The hosted preview does not accept
            personal files, planning data, business metrics, or cloud connections. Download the
            Windows app to work with your own data.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_demo_access(settings: Settings) -> None:
    _render_page_intro(
        "Workspace access",
        "Test the decisions, not the setup.",
        "Open one of three preloaded business situations and follow the evidence from source "
        "data to decision.",
    )
    _render_access_panel(settings)


def render_product_page(settings: Settings) -> None:
    """Render the public Costavow product experience before the analytical workspace."""
    st.html(PRODUCT_PAGE_CSS)

    selected_page = st.session_state.get("product_page", "Product")
    if selected_page not in PUBLIC_PAGES:
        selected_page = "Product"
        st.session_state["product_page"] = selected_page

    if selected_page == "Demo":
        _render_demo_access(settings)
    else:
        _render_overview(settings)
        _render_pipeline()
        _render_trust()

    st.markdown(
        '<div class="metrora-product-footer">'
        "Costavow - FinOps decision evidence - local product preview"
        "</div>",
        unsafe_allow_html=True,
    )
