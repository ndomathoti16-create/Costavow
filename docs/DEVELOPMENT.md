# Run and develop Costavow

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
git clone https://github.com/ndomathoti16-create/Costavow.git
cd Costavow
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -e ".[dev]"
```

macOS or Linux, for the browser workspace:

```bash
git clone https://github.com/ndomathoti16-create/Costavow.git
cd Costavow
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
`run-costavow.cmd` starts the same preview on port 8502 using the repository's virtual environment.

### Deploy the public Costavow website

The public project website is plain HTML/CSS in `site/`, published to
`https://ndomathoti16-create.github.io/Costavow/`. GitHub Pages must use **GitHub Actions**
as its build source. The `website` job in CI publishes only after both Python jobs pass,
including real-browser checks on Python 3.12. It uploads only `site/`; no Python runtime,
configuration secrets, or local analysis data are published with the static page.

The interactive demo remains at `https://costavow.streamlit.app/`. Its Community Cloud settings are:

| Setting | Value |
| --- | --- |
| Repository | `ndomathoti16-create/Costavow` |
| Branch | `main` |
| Main file | `app.py` |
| Python | `3.12` |
| App URL | `costavow.streamlit.app` |

Leave `COSTAVOW_DESKTOP` and `METRORA_DESKTOP` unset. The public demo needs no cloud or AI secrets.
It opens the scenario chooser; existing workspace query URLs continue to work.

Community Cloud deployment coordinates do not automatically follow every repository rename.
If the app stops receiving updates after a rename, inspect its repository, branch, and entrypoint;
follow [Streamlit's rename/redeployment guidance](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/rename-your-app).
Re-pushing code or changing only the subdomain does not repair stale repository coordinates.

### Preview and check the design

Use three terminals from the repository root, with the Python environment active:

```text
python -m streamlit run app.py --server.address=127.0.0.1 --server.port=8527
```

```text
python -m http.server 8528 --bind 127.0.0.1 --directory site
```

```text
npm ci --ignore-scripts
npx playwright install chromium
npm run test:browser
```

The browser check visits the website and every workspace destination at 320, 390, 768, 1024,
1440, and 1920 pixels. It checks page overflow, metric truncation, evidence-row overlap, chart
labels and legends, keyboard entry, native FAQs, image loading, hosted upload restrictions,
and an actual receipt download. Screenshots are saved under ignored `build/browser-checks/`.
For an existing Edge installation, set `COSTAVOW_BROWSER_PATH` to its executable path.
Playwright is a development dependency only; the public website ships no JavaScript.

The website screenshots are authentic synthetic workspace captures. Refresh both desktop and
mobile images when their represented UI changes; keep the image dimensions in `site/index.html`
accurate. Desktop screenshots should stop at a complete component, not crop text or controls.

## Configuration and external services

[.env.example](../.env.example) lists placeholders. Costavow reads process environment variables;
it does **not** automatically load a `.env` file. Use your shell or deployment environment to set them.

| Setting | Use |
| --- | --- |
| `APP_ENV`, `LOG_LEVEL` | Environment label and logging level. |
| `DATA_DIR`, `DB_PATH` | Local state directory and DuckDB file. Defaults for plain Streamlit are under `./data`. |
| `MAX_UPLOAD_MB` | Import limit; defaults to 200 MiB and also bounds supported expansion/table checks. |
| `COSTAVOW_DESKTOP` | Set to `1` for local data workflows; leave unset for the hosted-style demo. |
| `COSTAVOW_USER_DATA_DIR` | Override the native launcher's per-user storage root. |
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

The workflow generates third-party notices, builds with [costavow.spec](../packaging/costavow.spec),
and packages `Costavow-Windows-x64.zip` with `SHA256SUMS.txt`. Review license texts, missing-license
markers, launch behavior, checksums, and unsigned-executable handling before distribution.

## Scope and limitations

This repository does not yet implement tenant authentication, application-level encryption,
automatic retention, or multi-writer transactional state. Size checks do not isolate parsers at the
OS level. Budget overlap, period alignment, business-metric coverage, floating-point arithmetic,
and model uncertainty are documented in [metric definitions](METRIC_DEFINITIONS.md).

## Rebrand compatibility

Costavow replaces the visible Metrora identity in current source. Existing v0.2.3 downloads and
screenshots retain their original name. The current interactive demo is `costavow.streamlit.app`;
the static project website is `https://ndomathoti16-create.github.io/Costavow/`.
Legacy `METRORA_DESKTOP`, `METRORA_USER_DATA_DIR`, `metrora-desktop`, `metrora-check`, and
`run-metrora.cmd` remain supported; the new environment names take precedence. Existing database
filenames, desktop data directories, Docker volume names, and decision IDs remain unchanged so a
rename does not orphan user data. Internal CSS selectors retain their old prefix.

Future release builds use `packaging/costavow.spec`, `Costavow.exe`, and
`Costavow-Windows-x64.zip`. The current release is `v0.3.1`; historical Metrora packages remain available in older releases.


### Release verification

A `v*` tag runs the Windows release workflow and prepares a **draft** release with the ZIP and
SHA-256 checksum. Before publishing the draft, download and verify the checksum, extract all files,
and test `Costavow.exe` on Windows with a synthetic billing export. Check automatic analysis,
navigation, forecast traces, and receipt/report downloads. Publish the verified draft from GitHub
Releases; retain earlier release assets unchanged.
