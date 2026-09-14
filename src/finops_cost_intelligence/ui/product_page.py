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
from .navigation import set_workspace_route

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


def render_product_page(settings: Settings) -> None:
    """Open the synthetic workspace; the public project story lives on GitHub Pages."""
    st.html("""
        <section class="costavow-demo-intro">
            <span class="metrora-section-kicker">THE INTERACTIVE WORKSPACE</span>
            <h1>Follow the evidence.</h1>
            <p>Choose a business situation. Explore its billing, test the forecast,
            and open the decision receipt. The data is already connected.</p>
        </section>
    """)
    with st.container(key="demo-scenarios"):
        columns = st.columns(len(DEMO_SCENARIOS), gap="medium")
        for index, (column, (scenario_id, scenario)) in enumerate(
            zip(columns, DEMO_SCENARIOS.items(), strict=True), start=1
        ):
            with column:
                with st.container(border=True, key=f"scenario-{scenario_id}"):
                    st.html(f"""
                        <article class="costavow-scenario">
                            <span class="metrora-section-kicker">0{index} / {escape(scenario["status"])}</span>
                            <h2>{escape(scenario["label"])}</h2>
                            <p>{escape(scenario["description"])}</p>
                            <p class="costavow-scenario-lesson">{escape(scenario["lesson"])}</p>
                        </article>
                    """)
                    if st.button(
                        f"Open {scenario['label'].lower()}",
                        type="primary" if scenario_id == DEFAULT_DEMO_SCENARIO else "secondary",
                        width="stretch",
                        key=f"product_demo_scenario_{scenario_id}",
                    ):
                        try:
                            activate_demo_session(settings, scenario_id)
                        except IngestionError as exc:
                            st.error(str(exc))
                        else:
                            st.rerun()
    st.html("""
        <aside class="costavow-demo-boundary">
            <strong>Synthetic data. Real calculations.</strong>
            <p>This hosted demo accepts no uploads or cloud connections. Decision edits
            stay in this browser session. Use the Windows app to work with your own exports.</p>
            <a href="https://github.com/ndomathoti16-create/Costavow/releases/latest"
               target="_blank" rel="noopener noreferrer">Download Costavow for Windows ↗</a>
        </aside>
    """)
