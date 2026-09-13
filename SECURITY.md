# Security policy

## Supported version

Security fixes are applied to the latest published release and the current `main` branch. Older
portable builds should be replaced rather than treated as supported long-term versions.

## Report a vulnerability

Use GitHub's private vulnerability reporting option in this repository's **Security** tab. Do not
include exploit details, credentials, customer data, or billing exports in a public issue. If the
private form is unavailable, open a minimal issue requesting a private contact channel without
describing the vulnerability.

Include the affected version, operating system, reproduction conditions, impact, and the smallest
safe proof of concept. Reports made in good faith will be reviewed as time permits.

## Security boundaries

- The hosted demo is synthetic and read-only.
- The desktop app binds its local Streamlit service to `127.0.0.1` and opens it in a private desktop
  webview session.
- Saved cloud profiles contain locations and identity selectors, not passwords, tokens, access
  keys, or service-account contents.
- File and cloud import sizes are bounded, including gzip and Excel/Parquet expansion checks.
  Parsed tables are also checked against the configured limit. Parsing still occurs in-process;
  these checks are not a hard operating-system memory or CPU sandbox.
- Azure identity credentials are only used with canonical HTTPS Azure Blob Storage account URLs.
- Optional remote AI endpoints require HTTPS, except for explicit loopback development services.
  Requests refuse redirects, cap responses at 1 MiB, and validate the returned summary structure.
  These checks do not establish that every generated statement is true.
- Financial values are calculated before any optional narrative request.

Users remain responsible for least-privilege IAM, endpoint security, credential rotation, device
encryption, backup controls, and validating exported reports before business use.

## Safe configuration

Never commit `.env`, Streamlit secrets, cloud credentials, private keys, real billing exports, or
customer identifiers. Verify release checksums, keep the desktop app current, and use synthetic or
anonymized data when reproducing a problem.

The desktop workspace has no application-level user authentication or tenant authorization. Keep
it bound to loopback on a trusted device. A shared deployment needs authentication, authorization,
rate limits, transactional state, organizational retention rules, and an independent security review.
