# Privacy

Costavow has a static project website, a hosted synthetic demo, and a local desktop workspace.

## Public project website

The GitHub Pages website serves static HTML, CSS, the project logo, and synthetic screenshots.
It includes no analytics, tracking scripts, third-party fonts, forms, or application storage.
GitHub may process connection logs under its own privacy practices. Following a demo or download
link opens Streamlit or GitHub, whose service terms and privacy practices apply.

## Hosted product demo

The public Streamlit deployment uses synthetic demonstration data. Demo decision edits remain
in browser-session state and do not update a shared decision store. It uses bundled synthetic data and
does not expose file upload, cloud connection, mapping changes, provider recommendation import, or
external AI controls. The hosting provider may still process normal service information such as IP
addresses, browser details, and operational logs under its own terms and privacy practices.

Do not submit confidential information through bug reports, screenshots, URLs, or other public
project channels.

## Desktop application

The desktop app performs its analytical work locally. By default, application data is stored under
`%LOCALAPPDATA%\Metrora` on Windows, including the DuckDB database, non-secret connection profiles,
decision records, and local diagnostic logs. Closing Costavow and deleting that folder removes its
local application state.

Costavow does not include application telemetry and does not store cloud passwords, access keys,
API tokens, or service-account files in its own connection profiles. Cloud SDKs and command-line
tools may maintain authentication caches outside Costavow; those remain governed by the provider's
tools and your operating-system account.

Application-initiated external transfers require a user action or a previously enabled refresh-on-open setting:

- a cloud refresh reads billing exports through the configured provider SDK; refresh-on-open repeats this when enabled in a saved connection;
- an optional S3 export writes the selected canonical dataset to the configured bucket; or
- an optional desktop AI request sends the calculated fact pack to the configured HTTPS provider.

The application files are not independently encrypted. Use an access-controlled Windows account,
device encryption such as BitLocker, least-privilege cloud roles, and approved organizational data
handling practices for sensitive billing data.

## Logs and support material

Application crash reports contain the exception type and stack frame basenames, function names,
and line numbers; exception messages and source lines are omitted. Third-party service logs may
still contain exception messages and local paths. Review and redact logs before sharing. Screenshots and exported reports may contain billing values or identifiers;
treat them with the same controls as the source data.

Local data and logs remain until you delete them; there is no automatic expiry. Decision records
can include owner names, notes, account IDs, and resource IDs. Optional AI fact packs can include
source names, service names, ownership labels, and financial totals. Approve the configured
provider and its retention terms before transmitting organizational data. JSON state assumes a
single local writer; atomic file replacement is not a multi-user transaction system.

This notice describes the current reference implementation and should be reviewed again before any
multi-user or commercial deployment.

Decision receipts include financial values, source and account/resource references, owner labels,
and decision notes selected from the current record. They are generated locally and downloaded
only on request. Review the file before sharing; it is not encrypted or an immutable audit log.
