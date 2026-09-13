# Run and develop Metrora

[Documentation index](README.md) · [Project overview](../README.md)

## Requirements

Use Python 3.11 or newer. CI verifies Python 3.11 and 3.12 on Linux; the release workflow builds on
Windows with Python 3.12. A native source-built desktop window also needs a working pywebview system
backend. The packaged Windows release includes its Python dependencies.

Run commands from the repository root. `requirements.txt` pins the verified Streamlit runtime;
use it for development, CI, containers, and release builds so rendering does not change implicitly.
The development extra also updates Setuptools to the minimum patched build-tool version.

## Python setup

PowerShell:

```powershell
git clone https://github.com/ndomathoti16-create/Metrora.git
cd Metrora
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -e ".[dev]"
```

macOS or Linux, for the browser workspace:

```bash
git clone https://github.com/ndomathoti16-create/Metrora.git
cd Metrora
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -e '.[dev]'
```

Synthetic demo files are already included. Regenerate them only when changing the fixture design:

```text
python data/demo/generate_demo_data.py
```

## Choose a local surface

### Product preview

```text
python -m streamlit run app.py --server.address=127.0.0.1
```

This opens the synthetic product demo. It does not enable real-data uploads. On Windows,
`run-metrora.cmd` starts the same preview on port 8502 using the repository's virtual environment.

### Real-data browser workspace

PowerShell:

```powershell
$env:METRORA_DESKTOP = "1"
python -m streamlit run app.py --server.address=127.0.0.1
```

macOS or Linux:

```bash
METRORA_DESKTOP=1 python -m streamlit run app.py --server.address=127.0.0.1
```

Open the local URL printed by Streamlit. `METRORA_DESKTOP=1` enables file uploads and local workflow
controls; it is a mode selector, not authentication. Keep this workspace on a trusted local device.
Unset that variable to return to the product preview.

### Native Windows window

```powershell
python -m pip install -r requirements.txt -e ".[cloud,desktop,dev]"
metrora-desktop
```

The native launcher chooses a loopback port and sets up per-user storage. Unlike a plain Streamlit
launch, it normally uses `%LOCALAPPDATA%\Metrora` rather than the repository's `data/` directory.

### Docker workspace

```text
docker compose up --build
```

Open [localhost:8501](http://localhost:8501). Compose enables the real-data workspace, binds the host
port to loopback, and stores application state in a named volume. The container runs as a non-root
user. Stop it with `docker compose down`; the volume remains. The default image supports file
analysis and AWS through boto3; Azure/GCP need the optional cloud SDKs and approved identity setup.

## Configuration and external services

[.env.example](../.env.example) lists placeholders. Metrora reads process environment variables;
it does **not** automatically load a `.env` file. Use your shell or deployment environment to set them.

| Setting | Use |
| --- | --- |
| `APP_ENV`, `LOG_LEVEL` | Environment label and logging level. |
| `DATA_DIR`, `DB_PATH` | Local state directory and DuckDB file. Defaults for plain Streamlit are under `./data`. |
| `MAX_UPLOAD_MB` | Import limit; defaults to 200 MiB and also bounds supported expansion/table checks. |
| `METRORA_DESKTOP` | Set to `1` for local data workflows; leave unset for the hosted-style demo. |
| `METRORA_USER_DATA_DIR` | Override the native launcher's per-user storage root. |
| `AI_PROVIDER`, `AI_MODEL`, `AI_API_KEY`, `AI_BASE_URL` | Optional narrative provider. AI is disabled by default; the adapter supports `openai`/`openai-compatible`. |
| `AWS_REGION`, `S3_BUCKET` | Optional canonical Parquet export. |
| `ATHENA_DATABASE`, `ATHENA_OUTPUT_LOCATION` | Settings available for programmatic Athena integration; there is no automatic Athena query UI. |

Install provider SDKs for source-based cloud connections:

```text
python -m pip install -r requirements.txt -e ".[cloud,dev]"
```

- **AWS:** configure a provider-managed billing export to S3 and use an AWS profile/role. Import needs
  `s3:ListBucket` and `s3:GetObject`; recommendation intake also needs
  `cost-optimization-hub:ListRecommendations`. Optional S3 export needs `s3:PutObject`.
- **Azure:** configure Cost Management export to Blob Storage. Use Azure CLI or managed identity
  with Storage Blob Data Reader and a canonical HTTPS Azure account URL.
- **GCP:** enable Cloud Billing export to BigQuery. Use Application Default Credentials with
  BigQuery Job User and Data Viewer. Query charges and provider retention policies still apply.

Saved profiles contain locations and identity selectors. Refresh-on-open repeats a previously
enabled connection; it does not schedule the provider's export. AI fact packs can include financial
values and identifiers. Review [PRIVACY.md](../PRIVACY.md) before enabling external processing.

## Verify changes

```text
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q app.py desktop.py src tests data/demo packaging
python -m bandit -q -r src app.py
python -m pip_audit --local
```

If pip-audit fails decoding a Windows path, set `$env:PYTHONUTF8 = "1"` and retry. The
[CI workflow](../.github/workflows/ci.yml) runs the checks on Python 3.11 and 3.12. It does not make
live cloud calls. Use synthetic fixtures and keep credentials, user uploads, and generated builds
out of Git.

## Build a Windows release

Use the **Windows desktop release** workflow's manual dispatch to build a test artifact. For a
published release, first update the package version and changelog, verify CI, then publish a matching
version tag. A new commit on `main` does not replace an existing release ZIP.

The workflow generates third-party notices, builds with [metrora.spec](../packaging/metrora.spec),
and packages `Metrora-Windows-x64.zip` with `SHA256SUMS.txt`. Review license texts, missing-license
markers, launch behavior, checksums, and unsigned-executable handling before distribution.

## Scope and limitations

This repository does not yet implement tenant authentication, application-level encryption,
automatic retention, or multi-writer transactional state. Size checks do not isolate parsers at the
OS level. Budget overlap, period alignment, business-metric coverage, floating-point arithmetic,
and model uncertainty are documented in [metric definitions](METRIC_DEFINITIONS.md).
