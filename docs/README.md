# Documentation

[Project overview](../README.md) · [Changelog](../CHANGELOG.md)

## Use and operate the current application

| Guide | Purpose |
| --- | --- |
| [Run and develop Metrora](DEVELOPMENT.md) | Source setup, demo/workspace modes, Docker, cloud identities, checks, and release builds. |
| [Data dictionary](DATA_DICTIONARY.md) | Accepted files, canonical columns, and lineage. |
| [Metric definitions](METRIC_DEFINITIONS.md) | Formulas, cost basis, currencies, and analytical caveats. |
| [Synthetic demo data](../data/demo/README.md) | The three scenarios and their matching supporting files. |
| [Privacy](../PRIVACY.md) | Local storage, external transfers, logs, and retention. |
| [Security](../SECURITY.md) | Safe configuration, trust boundaries, and private vulnerability reports. |
| [Third-party notices](../THIRD_PARTY_NOTICES.md) | Dependency attribution and release inventory requirements. |
| [Code review](CODE_REVIEW.md) | The cleanup's local verification record and remaining assumptions. |

## Architecture and optional integrations

- [AWS extension architecture](AWS_ARCHITECTURE.md): implemented adapters and proposed cloud flow.
- [AWS setup notes](../infra/aws/README.md): optional S3, Glue, and Athena configuration.
- [Project plan](PROJECT_PLAN.md): original milestones and design intent, preserved as project history.

## Research and background

These documents explain design decisions and proposed directions. They are not current setup
instructions, release promises, or a continuously updated market comparison.

- [Productization research](PRODUCTIZATION_RESEARCH.md)
- [Product UX research](PRODUCT_UX_RESEARCH.md)
- [Differentiation strategy](DIFFERENTIATION_STRATEGY.md)
- [Interview notes](INTERVIEW_NOTES.md)

[Assets](assets/) contains the project mark. [Screenshots](screenshots/) contains v0.2.3 product and
workspace captures; new source calculations may differ from those images.
