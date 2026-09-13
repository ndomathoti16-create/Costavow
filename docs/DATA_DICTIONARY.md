# Data dictionary

## Cloud billing input

Billing uploads may use provider-specific names. Automatic mapping and normalization produce
the canonical model; optional persistence writes it to `fact_cloud_cost`. Accepted local formats
are CSV, XLSX, XLS, and Parquet. Cloud export connectors also accept CSV.GZ.

| Canonical field | Required | Meaning |
|---|---:|---|
| `usage_date` | Yes | UTC calendar day assigned to the charge or usage; naive timestamps are treated as UTC |
| `service` | Yes | Cloud service or product family |
| `cost` | Yes | Monetary amount used for analysis |
| `currency` | No | Currency code; mixed currencies block analysis |
| `provider` | No | Cloud provider |
| `account_id` / `account_name` | No | Cloud account or subscription identity |
| `region` | No | Region or global scope |
| `resource_id` / `resource_name` | No | Provider resource identifier and display name |
| `department` | No | Owning department or cost center |
| `project` | No | Product, application, or workload |
| `environment` | No | Production, staging, development, or similar |
| `usage_quantity` / `usage_unit` | No | Provider usage measure |
| `usage_type` / `cost_type` | No | Provider charge classification |
| `tags_json` | No | Original tag payload preserved for lineage |

The application adds `ingestion_id`, `source_file`, `source_row_number`, and `source_row_hash` for lineage.

## Budget input

Required fields are `period_start` and `budget_amount`. If omitted, `period_end` defaults to
month-end, `scope_type` to `total`, and `currency` to `Unspecified`. Non-total scopes require
`scope_value`. Common aliases such as `month`, `budget`, `dimension`, and `value` are accepted.
Supported scopes are total, service, account_id (or the alias account), department, project,
environment, and region. Currency assumptions and overlapping budgets require review; see
[metric definitions](METRIC_DEFINITIONS.md).

## Business metric input

Required fields are `metric_date`, `metric_name`, and `metric_value`; `unit` defaults to `units`. The application aggregates duplicate rows to daily metric grain before calculating cost per unit. A user selects one metric explicitly; unrelated metrics are not silently combined.
