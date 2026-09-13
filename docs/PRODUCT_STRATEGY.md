# Costavow: market review and product scope

Reviewed 2026-09-13. This is a representative comparison of direct and adjacent products using
public first-party material, not an exhaustive inventory or a hands-on vendor benchmark.
Capabilities change; absence from a product page is not evidence that a feature is missing.

## What similar products already do well

| Product or family | Documented strengths | Implication for this project |
| --- | --- | --- |
| [Vantage](https://www.vantage.sh/features) | Cost reports, budgets, virtual tags, unit costs, optimization, and AI workflows. | Another dashboard or chat assistant is not a persuasive distinction. |
| [CloudZero](https://docs.cloudzero.com/docs/unit-economics) | Business-unit cost measures with multiple allocation dimensions and telemetry. | Unit economics is expected analytical context, not an exclusive feature. |
| [Finout](https://docs.finout.io/user-guide/inform/virtual-tags/finout-virtual-tags-alpha) | Normalized cross-cloud dimensions and virtual tags. | Keep a clear cost contract; do not imply that normalization is novel. |
| [IBM Cloudability](https://www.ibm.com/docs/en/cloudability-commercial/cloudability-standard/saas?topic=optimize-optimization-dashboard) | Resource and commitment optimization opportunities. | Preserve provider estimates and their basis rather than inventing optimization telemetry. |
| [Harness](https://www.harness.io/products/cloud-ai-cost-management) | Visibility, governance, and automated optimization, including commitments. | Resource-changing automation needs a different operational and security scope. |
| [Infracost](https://www.infracost.io/docs/infracost_cloud/engineer_guide/) | Cost changes and policy feedback in infrastructure pull requests. | This project starts from billing actuals; infrastructure planning is a separate job. |
| [OpenCost](https://opencost.io/docs/specification/) | Vendor-neutral Kubernetes infrastructure and container allocation. | Billing-only data cannot replace workload allocation telemetry. |
| [AWS Cost Optimization Hub](https://docs.aws.amazon.com/cost-management/latest/userguide/cost-optimization-hub.html) | Consolidated native recommendations using AWS commercial terms. | Reuse the existing read-only recommendation adapter. |
| [Azure Advisor](https://learn.microsoft.com/en-us/azure/advisor/advisor-overview) | Recommendations based on resource configuration and usage telemetry. | Accept manually sourced recommendations without claiming a direct adapter exists. |
| [Google Cloud FinOps hub](https://docs.cloud.google.com/billing/docs/how-to/finops-hub) | Billing, utilization, and optimization recommendations. | Keep GCP billing import distinct from recommendation integration. |
| [Microsoft FinOps toolkit](https://learn.microsoft.com/en-us/cloud-computing/finops/toolkit/finops-toolkit-overview) | Customizable tools and reports that extend Microsoft Cost Management. | Open, inspectable reporting already exists; local execution alone is not unique. |
| [Powerpipe AWS Cost and Usage Insights](https://hub.powerpipe.io/mods/turbot/tailpipe-mod-aws-cost-usage-report-insights/dashboards) | Prebuilt cost and usage dashboards. | Show the complete decision handoff, not just a collection of charts. |

## The deliberate point of difference

**A small, local reference application where a reviewer can follow a cost claim from input checks
through a human decision to a supplied outcome, then take that record away.**

This is positioning based on the code's strengths, not a claim of an unoccupied market, superior
enterprise capability, or exclusive intellectual property. The primary audience is an analyst,
engineer, or technical reviewer who wants to inspect how the system reaches and qualifies a result.
It also makes the project's engineering decisions visible to a hiring reviewer.

## The addition justified by the research

The existing application already had reconciliation, financial classifications, owner/status
tracking, outcome comparisons, and CSV/JSON exports. The gap was a readable handoff for one action.
The **decision receipt** adds that handoff using the existing record and Python's standard library:

- Source and ingestion references, fact IDs, evidence classification, and financial basis.
- Owner, timing, disposition, notes, and missing information.
- Supplied baseline/post-change periods and amounts, with the signed difference.
- Explicit limits: no causal attribution, no automatic annualization, no independent verification,
  and no claim of an immutable audit log. Financial and identifying details require review before sharing.

The synthetic demo exposes the same receipt without credentials or new external services. A
related correctness fix prevents adding outcome values across unknown or mixed currencies.

## How to evaluate the implementation

1. Launch the Hidden future risk synthetic scenario and inspect the source reconciliation and quality report.
2. Trace a calculated recommendation into [decision creation](../src/finops_cost_intelligence/decisions/services.py).
3. Review how evidence refresh preserves human disposition and existing stable IDs.
4. Download a receipt from Decisions, compare its references with the fact-pack export, and inspect
   [the small renderer](../src/finops_cost_intelligence/decisions/receipt.py).
5. Run [decision tests](../tests/test_decisions.py) and [boundary regressions](../tests/test_review_regressions.py).
   These exercise escaped inputs, estimate/actual separation, negative outcomes, and currency boundaries.

This demonstrates data modeling, financial reasoning, state design, secure exports, product scope,
and regression testing. It makes no claim about commercial adoption or independently audited savings.

## What was intentionally not added

No chatbot, additional provider SDK, savings leaderboard, new dashboard page, cloud-resource
mutation, shared accounts, or notification service. Add integrations only when a real input cannot
be represented by the existing contract. Add shared access only with an explicit multi-user need,
authorization model, and transactional history. Stronger outcome attribution requires comparable
usage and scope evidence; a rebrand cannot supply that evidence.

The earlier [differentiation document](DIFFERENTIATION_STRATEGY.md) remains historical planning.
This review narrows the immediate scope instead of treating its roadmap as a feature checklist.
