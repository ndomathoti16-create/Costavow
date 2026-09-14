# Third-party notices

Costavow depends on third-party Python packages and GitHub Actions listed in `pyproject.toml` and the
workflow files under `.github/workflows`. Those components remain subject to their respective
licenses and notices. Installing optional `cloud`, `desktop`, or `dev` extras adds the corresponding
provider SDK, desktop runtime, packaging, and verification dependencies.

The interface uses operating-system font fallbacks and does not download web fonts at runtime.
Product screenshots and the Costavow SVG mark in this repository are project assets rather than
stock imagery.

The Windows release workflow generates `THIRD_PARTY_LICENSES.txt` from the exact build environment
and includes it alongside this notice in the portable application. The generated inventory should
be reviewed whenever dependencies change and before redistributing a build.

The generator collects modern `dist-info/licenses` files, legacy license files, and packaged
LICENSE/COPYING/NOTICE texts. A missing license text is explicitly marked for verification.
Regenerate the bundle from the release build environment before redistributing; an inventory does
not by itself establish permission or satisfy every component's attribution obligations.

The application uses standard-library configuration, so Pydantic, pydantic-settings, and
python-dotenv are no longer direct requirements. NumPy was already required by the numerical
stack and is now declared explicitly because application code imports it. GitPython's minimum
version constraint remains in place for Streamlit's transitive dependency.


For installed wheels that omit notice text, the generator includes reviewed, exact-version copies
from `packaging/licenses/`, each with an immutable upstream source URL. In particular,
`proxy_tools` 0.1.0 declares MIT in its metadata but supplies a BSD-style license in its upstream
repository. The complete upstream notice is preserved; metadata alone is not treated as the grant.
No new dependency is introduced by this supplement.

Browser verification uses Playwright (Apache-2.0), pinned with its dependencies in `package-lock.json`.
It is development tooling and is not included in the static site or Windows executable. The npm
packages retain their own LICENSE and NOTICE files when installed. See
[Playwright's license](https://github.com/microsoft/playwright/blob/v1.62.1/LICENSE) and
[notices](https://github.com/microsoft/playwright/blob/v1.62.1/NOTICE).
