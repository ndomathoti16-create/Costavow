# Metric definitions

All monetary values come from the normalized canonical `cost` field and are calculated before the summary layer runs.

## Cost-basis policy

The accepted field mapping records the source column behind `cost`; every reconciliation,
chart, forecast, anomaly, recommendation, and export uses that same basis. For a FOCUS 1.3
export containing both fields, Metrora automatically proposes `EffectiveCost` because FOCUS
defines it as the amortized cost after discounts and prepaid-purchase allocation and identifies
it as a common basis for spend trends. A reviewer can select `BilledCost` in Data settings for
cash-basis budgeting, invoice alignment, or payable reconciliation. Metrora never combines the
two bases or silently changes basis within an analysis.

| Metric | Definition | Caveat |
|---|---|---|
| Total spend | Sum of `cost` in the selected period and filters | Currency must be consistent |
| Average daily spend | Total spend divided by inclusive calendar days | Zero-cost calendar days remain in the denominator |
| Period variance | Actual matched amount minus budget amount | Positive means actual is above budget |
| Budget utilization | Actual matched amount divided by budget amount | Undefined when budget is zero |
| Allocation row coverage | Rows with a populated ownership field divided by all selected rows | Field selection is user-controlled |
| Allocation cost coverage | Positive spend with a populated ownership field divided by positive spend | Credits and refunds are excluded from the denominator |
| Cost per business unit | Selected-period cloud cost divided by selected business metric total | Requires daily-grain metric data and a non-zero denominator |
| Forecast total | Sum of daily forecasts across the selected horizon | Method and residual variation are shown |
| Anomaly score | Deviation from prior rolling median scaled by prior rolling MAD or standard deviation | The observed day is excluded from its own baseline |

Comparisons are inclusive by date. The dashboard exposes the selected period, filters, currency label, quality status, forecast method, and anomaly threshold with the results.

Billing timestamps are converted to UTC calendar days; naive timestamps are treated as UTC.
Non-finite numeric values are rejected as invalid rather than included in financial totals.

MAD is the median absolute distance from the median of the same prior window. When MAD is zero,
the detector uses that window's sample standard deviation. This correction can change anomaly
counts relative to earlier releases, including the synthetic forecast-risk scenario.

Budget comparisons reject conflicting populated currencies. An omitted currency still requires a
human comparability assumption. Budget summaries sum the supplied rows: overlapping total and
service budgets can count the same actual spend more than once, and full budget amounts are not
prorated for partial billing periods. Supply non-overlapping, period-aligned budgets for a combined
portfolio total.

Unit economics restrict business volume to the selected billing calendar window. The ratio uses
dates represented in the selected metric; ensure complete daily coverage and an additive metric
before interpreting it as a whole-period unit cost. Do not sum stock metrics such as an end-of-day
customer count and interpret the result as unique customers. The selected metric must use one unit.
