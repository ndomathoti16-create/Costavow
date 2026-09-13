"""A self-contained, escaped handoff for one decision; no remote assets or scripts."""

from __future__ import annotations

from html import escape

from .models import DecisionRecord


def decision_receipt_html(decision: DecisionRecord) -> str:
    """Render the supplied record without claiming causal or independent verification."""

    def amount(value: float | None) -> str:
        return (
            "Not supplied"
            if value is None
            else f"{decision.currency or 'Unspecified'} {value:,.2f}"
        )

    fields = [
        ("Decision ID", decision.decision_id),
        ("Status", decision.status),
        ("Owner", decision.owner),
        ("Due", decision.due_date or decision.target_timing),
        ("Updated", decision.updated_at),
        ("Source type", decision.source_kind),
        ("Source reference", decision.source_reference),
        ("Source file", decision.metadata.get("source_name", "Not supplied")),
        ("Ingestion reference", decision.metadata.get("ingestion_id", "Not supplied")),
        ("Fact references", decision.metadata.get("fact_ids", "Not supplied")),
        (
            "Provider / account / resource",
            " / ".join(
                filter(None, [decision.provider, decision.account_id, decision.resource_id])
            ),
        ),
        ("Evidence", decision.evidence_summary),
        ("Evidence classification", decision.evidence_strength.replace("_", " ")),
        ("Financial basis", decision.impact_kind.replace("_", " ")),
        ("Signal or estimate", amount(decision.impact_amount)),
        ("Decision note / caveats", decision.decision_note or "Not supplied"),
        ("Rejection reason", decision.rejection_reason or "Not applicable"),
        ("Baseline period", decision.baseline_period or "Not supplied"),
        ("Baseline actual", amount(decision.baseline_cost)),
        ("Measurement period", decision.measurement_period or "Not supplied"),
        ("Post-change actual", amount(decision.post_change_cost)),
        ("Baseline minus post-change", amount(decision.actual_cost_change)),
    ]
    rows = "".join(
        f"<tr><th scope='row'>{escape(label)}</th><td>{escape(str(value))}</td></tr>"
        for label, value in fields
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src
'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Costavow decision receipt</title>
<style>
body{{margin:0;background:#f4f1e9;color:#142421;font:16px/1.6 system-ui,sans-serif}}
main{{max-width:880px;margin:32px auto;padding:32px;background:#fff;border-top:6px solid #b57e34}}
small{{letter-spacing:.12em;text-transform:uppercase;color:#466257}}
h1{{font-size:clamp(24px,5vw,36px);line-height:1.2;overflow-wrap:anywhere}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;text-align:left;vertical-align:top;border-bottom:1px
solid #ddd;overflow-wrap:anywhere}}
th{{width:30%;font-weight:600}}p{{max-width:75ch}}footer{{margin-top:24px;font-size:14px}}
@media(max-width:600px){{main{{margin:0;padding:20px}}th,td{{display:block;width:auto}}th{{border:0;padding-bottom:0}}}}
@media print{{body{{background:#fff}}main{{margin:0;padding:0}}tr{{break-inside:avoid}}}}
</style></head><body><main>
<small>Costavow / decision receipt</small><h1>{escape(decision.title)}</h1>
<p>Every cost claim needs a trail. This snapshot brings the source, human decision, and supplied
outcome together.</p>
<table><tbody>{rows}</tbody></table>
<footer><strong>How to read the result.</strong> Baseline minus post-change is a
supplied-actuals comparison:
positive means a reduction; negative means an increase. It is not an annualized estimate or proof
that the action caused the change. Review equal periods, scope, currency, usage, credits, and
seasonality.
A Verified status records a user's review; Costavow does not independently verify the inputs.
This is an editable snapshot, not a signed or immutable audit log.
<p>Contains financial values, identifiers, ownership, and notes. Review before sharing.</p></footer>
</main></body></html>"""
