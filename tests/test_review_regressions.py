"""Regression checks for the repository simplification and boundary review."""

import io
import json
import runpy
from dataclasses import replace
from email.message import Message
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
import pytest

from finops_cost_intelligence import desktop
from finops_cost_intelligence.ai import build_fact_pack, summarize_fact_pack
from finops_cost_intelligence.ai import client as ai_client
from finops_cost_intelligence.ai.summarizer import deterministic_summary
from finops_cost_intelligence.analytics.budgets import calculate_budget_variance
from finops_cost_intelligence.analytics.drivers import analyze_service_cost_drivers
from finops_cost_intelligence.analytics.spend import calculate_spend_summary
from finops_cost_intelligence.anomalies import detect_spend_anomalies
from finops_cost_intelligence.connections import ConnectionStore
from finops_cost_intelligence.contracts.analytics import AnalyticsInputError
from finops_cost_intelligence.contracts.budget import BudgetValidationError
from finops_cost_intelligence.contracts.business_metrics import BusinessMetricValidationError
from finops_cost_intelligence.decisions import DecisionStore, ranked_decisions
from finops_cost_intelligence.exports import executive_report_html
from finops_cost_intelligence.ingestion import FileTooLargeError, load_table, profile_table
from finops_cost_intelligence.ingestion.readers import LoadedTable, UnreadableFileError
from finops_cost_intelligence.normalization import normalize_billing_table
from finops_cost_intelligence.normalization.budgets import normalize_budget_dataframe
from finops_cost_intelligence.normalization.business_metrics import normalize_business_metrics
from finops_cost_intelligence.quality import run_quality_checks
from finops_cost_intelligence.ui.mapping_view import source_key_for
from tests.test_decisions import _decision
from tests.test_milestone7 import _run_with_evidence


def test_mad_uses_one_median_for_the_prior_window():
    data = pd.DataFrame(
        {"usage_date": pd.date_range("2025-01-01", periods=5), "cost": [1, 2, 3, 4, 10]}
    )
    diagnostics, _ = detect_spend_anomalies(data, window_days=4, minimum_history_days=4)
    last = diagnostics.iloc[-1]
    assert last["expected_cost"] == 2.5
    assert last["anomaly_score"] == pytest.approx(7.5 / 1.4826)
    assert last["is_anomaly"]
    data.loc[4, "cost"] = -10
    changed, _ = detect_spend_anomalies(data, window_days=4, minimum_history_days=4)
    assert changed.iloc[-1]["expected_cost"] == last["expected_cost"]
    assert changed.iloc[-1]["anomaly_score"] < 0


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), "Infinity"])
def test_nonfinite_financial_inputs_are_blocked(value):
    loaded = LoadedTable(
        pd.DataFrame({"date": ["2025-01-01"], "service": ["Compute"], "cost": [value]}),
        "synthetic.csv",
        "csv",
        None,
    )
    normalized = normalize_billing_table(
        loaded, {"usage_date": "date", "service": "service", "cost": "cost"}
    )
    assert normalized.report.issue_count == 1
    assert not run_quality_checks(loaded, normalized).ready_for_analysis
    with pytest.raises(BudgetValidationError):
        normalize_budget_dataframe(pd.DataFrame({"date": ["2025-01-01"], "budget": [value]}))
    with pytest.raises(BusinessMetricValidationError):
        normalize_business_metrics(
            pd.DataFrame({"date": ["2025-01-01"], "metric": ["Orders"], "value": [value]})
        )
    with pytest.raises(AnalyticsInputError):
        calculate_spend_summary(pd.DataFrame({"usage_date": ["2025-01-01"], "cost": [value]}))


def test_billing_normalizes_mixed_timezones_to_utc_calendar_days():
    loaded = LoadedTable(
        pd.DataFrame(
            {
                "date": ["2025-01-01T23:30:00-05:00", "2025-01-02"],
                "service": ["Compute"] * 2,
                "cost": [1, 2],
            }
        ),
        "synthetic.csv",
        "csv",
        None,
    )
    normalized = normalize_billing_table(
        loaded, {"usage_date": "date", "service": "service", "cost": "cost"}
    )
    assert normalized.dataframe["usage_date"].tolist() == [pd.Timestamp("2025-01-02")] * 2


def test_nested_tags_profile_and_source_identity_include_values():
    frame = pd.DataFrame({"service": ["Compute", "Compute"], "tags": [{"team": "A"}] * 2})
    loaded = LoadedTable(frame, "synthetic.parquet", "parquet", 100)
    profile = profile_table(loaded)
    assert profile.duplicate_row_count == 1
    assert profile.columns[1].unique_count == 1
    original = source_key_for(loaded, profile)
    frame.at[1, "tags"] = {"team": "B"}
    assert source_key_for(loaded, profile) != original


@pytest.mark.parametrize("suffix", ["xlsx", "parquet"])
def test_compressed_expansion_is_checked_before_parsing(suffix, monkeypatch):
    payload = io.BytesIO()
    if suffix == "xlsx":
        with ZipFile(payload, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr("xl/worksheets/sheet1.xml", "a" * 50000)
    else:
        pd.DataFrame({"value": range(10000)}).to_parquet(payload, compression="gzip")
    from finops_cost_intelligence.ingestion import readers

    def unexpected_parse(*args):
        pytest.fail("Expanded file should have been rejected before parsing")

    monkeypatch.setattr(readers, "_read_by_format", unexpected_parse)
    raw = payload.getvalue()
    with pytest.raises(FileTooLargeError, match="Expanded"):
        load_table(raw, source_name=f"synthetic.{suffix}", max_bytes=len(raw) + 100)


def test_parser_error_does_not_expose_underlying_exception(monkeypatch):
    from finops_cost_intelligence.ingestion import readers

    def fail(*args):
        raise ValueError("synthetic-secret-token")

    monkeypatch.setattr(readers, "_read_by_format", fail)
    with pytest.raises(UnreadableFileError) as error:
        load_table(b"a,b\n1,2", source_name="synthetic.csv")
    assert "synthetic-secret-token" not in str(error.value)


def test_ai_redirects_cannot_forward_credentials():
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread

    paths = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            paths.append(self.path)
            self.send_response(302)
            self.send_header("Location", "/collect")
            self.end_headers()

        def do_GET(self):
            paths.append(self.path)
            self.send_response(200)
            self.end_headers()

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            client = ai_client.OpenAICompatibleClient(
                api_key="synthetic-token",
                model="test",
                base_url=f"http://127.0.0.1:{server.server_port}",
            )
            with pytest.raises(ai_client.AIProviderError):
                client.complete("system", "synthetic facts")
            assert paths == ["/chat/completions"]
        finally:
            server.shutdown()
            worker.join(timeout=2)


@pytest.mark.parametrize(
    "raw",
    [
        b"\xff",
        b"[]",
        b'{"choices":[]}',
        b'{"choices":[{"message":{"content":null}}]}',
        b"x" * (ai_client.MAX_RESPONSE_BYTES + 1),
    ],
    ids=["invalid-utf8", "wrong-shape", "no-choices", "null-content", "oversized"],
)
def test_ai_unusable_responses_fail_safely(raw, monkeypatch):
    monkeypatch.setattr(
        ai_client,
        "build_opener",
        lambda *args: SimpleNamespace(open=lambda *args, **kwargs: io.BytesIO(raw)),
    )
    client = ai_client.OpenAICompatibleClient(api_key="synthetic-token", model="test-model")
    with pytest.raises(ai_client.AIProviderError):
        client.complete("system", "facts")


@pytest.mark.parametrize(
    "field,value",
    [
        ("headline", None),
        ("bullets", "text"),
        ("used_fact_ids", {}),
        ("caveats", None),
        ("bullets", ["text"] * 5),
    ],
)
def test_malformed_ai_summary_uses_deterministic_fallback(field, value):
    normalized, quality, _ = _run_with_evidence()
    facts = build_fact_pack(normalized, quality)
    payload = deterministic_summary(facts).to_dict()
    payload[field] = value
    client = SimpleNamespace(complete=lambda *args: json.dumps(payload))
    result = summarize_fact_pack(facts, client=client)
    assert result.provider == "deterministic_fallback"
    assert "failed validation" in result.caveats[-1]


@pytest.mark.parametrize("store_class", [ConnectionStore, DecisionStore])
@pytest.mark.parametrize(
    "payload",
    [[], None, {"version": 1}, {"version": 1, "connections": [None], "decisions": [None]}],
)
def test_malformed_store_fails_without_modifying_file(tmp_path, store_class, payload):
    path = tmp_path / "state.json"
    original = json.dumps(payload)
    path.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError):
        store_class(path).list()
    assert path.read_text(encoding="utf-8") == original


def test_crash_reports_exclude_sensitive_exception_content(tmp_path, monkeypatch):
    monkeypatch.setenv("METRORA_USER_DATA_DIR", str(tmp_path))
    try:
        raise ValueError("synthetic-secret-token")
    except ValueError as exc:
        path = desktop._write_crash_report(exc)
    report = path.read_text(encoding="utf-8")
    assert "ValueError" in report
    assert "test_review_regressions.py" in report
    assert "synthetic-secret-token" not in report
    assert str(tmp_path) not in report


def test_license_bundle_finds_modern_and_legacy_notices(tmp_path):
    paths = [
        "example.dist-info/licenses/LICENSE",
        "example.dist-info/licenses/AUTHORS",
        "legacy.dist-info/NOTICE",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Synthetic notice for regression testing", encoding="utf-8")
    metadata = Message()
    metadata["License-File"] = "LICENSE"
    metadata["License-File"] = "AUTHORS"
    distribution = SimpleNamespace(
        files=paths, metadata=metadata, locate_file=lambda name: tmp_path / name
    )
    module = runpy.run_path(
        str(Path(__file__).parents[1] / "packaging/generate_third_party_licenses.py")
    )
    texts = module["_license_texts"](distribution)
    assert {name for name, _ in texts} == set(paths)


def test_numeric_report_units_are_html_escaped():
    normalized, quality, _ = _run_with_evidence()
    facts = build_fact_pack(normalized, quality)
    malicious = replace(facts.facts[0], value=1, unit='<img src=x onerror="alert(1)">')
    facts = replace(facts, facts=(malicious, *facts.facts[1:]))
    report = executive_report_html(facts, deterministic_summary(facts))
    assert "<img src=x" not in report
    assert "&lt;img" in report


def test_budget_rejects_currency_mismatch_and_distinguishes_zero_actuals():
    actual = pd.DataFrame({"usage_date": ["2025-01-01"], "cost": [0], "currency": ["USD"]})
    budget = normalize_budget_dataframe(
        pd.DataFrame({"date": ["2025-01-01"], "budget": [10], "currency": ["EUR"]})
    )
    with pytest.raises(AnalyticsInputError, match="currencies"):
        calculate_budget_variance(actual, budget)
    budget["currency"] = "USD"
    comparison, _ = calculate_budget_variance(actual, budget)
    assert comparison.iloc[0]["status"] == "on_track"
    with pytest.raises(AnalyticsInputError, match="no rows"):
        calculate_budget_variance(actual, budget.iloc[:0])


def test_partial_usage_does_not_claim_comparable_usage_evidence():
    frame = pd.DataFrame(
        {
            "usage_date": ["2025-01-01", "2025-01-02", "2025-01-02"],
            "service": ["Compute"] * 3,
            "cost": [10, 10, 10],
            "usage_quantity": [1, 1, None],
            "usage_unit": ["hours"] * 3,
        }
    )
    movers = analyze_service_cost_drivers(
        frame,
        prior_start="2025-01-01",
        prior_end="2025-01-01",
        recent_start="2025-01-02",
        recent_end="2025-01-02",
    )
    assert movers.iloc[0]["driver_type"] == "Billing-only"


def test_closed_decisions_do_not_dilute_open_work_priority():
    current = _decision()
    closed = replace(
        current, decision_id="closed", status="Rejected", rejection_reason="Test", impact_amount=1e9
    )
    alone = ranked_decisions([current])[0][1]
    assert ranked_decisions([current, closed])[0][1] == alone


def test_atomic_state_write_keeps_previous_data_on_failure(tmp_path, monkeypatch):
    from finops_cost_intelligence.storage import local_json

    path = tmp_path / "state.json"
    path.write_text('{"original": true}', encoding="utf-8")

    def fail_replace(*args):
        raise OSError("Simulated replacement failure")

    monkeypatch.setattr(local_json.os, "replace", fail_replace)
    with pytest.raises(OSError):
        local_json.write_json_atomically(path, {"changed": True})
    assert json.loads(path.read_text()) == {"original": True}
    assert sorted(item.name for item in tmp_path.iterdir()) == ["state.json"]


def test_unit_economics_limits_volume_to_the_selected_billing_period():
    from finops_cost_intelligence.analytics.business_metrics import calculate_unit_economics

    actual = pd.DataFrame({"usage_date": ["2025-01-02"], "cost": [100]})
    metrics = normalize_business_metrics(
        pd.DataFrame(
            {"date": ["2025-01-01", "2025-01-02"], "metric": ["Orders"] * 2, "value": [90, 10]}
        )
    )
    _, summary = calculate_unit_economics(actual, metrics, "Orders")
    assert summary.total_metric_value == 10
    assert summary.cost_per_unit == 10


def test_zero_cost_reconciles_at_zero_tolerance():
    loaded = LoadedTable(
        pd.DataFrame({"date": ["2025-01-01"], "service": ["Compute"], "cost": [0]}),
        "synthetic.csv",
        "csv",
        None,
    )
    normalized = normalize_billing_table(
        loaded, {"usage_date": "date", "service": "service", "cost": "cost"}
    )
    report = run_quality_checks(loaded, normalized, reconciliation_tolerance=0)
    assert report.reconciliation.passed
    assert report.reconciliation.relative_difference == 0


def test_hosted_demo_does_not_offer_configured_external_actions(monkeypatch):
    from streamlit.testing.v1 import AppTest

    monkeypatch.delenv("METRORA_DESKTOP", raising=False)
    monkeypatch.setenv("S3_BUCKET", "synthetic-test-bucket")
    monkeypatch.setenv("AI_PROVIDER", "openai")
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.query_params.update({"surface": "workspace", "page": "Reports", "scenario": "healthy"})
    app.run(timeout=30)
    assert not app.exception
    labels = {item.label for item in app.button}
    assert "Upload canonical Parquet to S3" not in labels
    assert "Refresh narrative with configured AI" not in labels
