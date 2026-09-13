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
