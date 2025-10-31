<!--
Guidance for AI coding agents (Copilot-style) to be productive in this repository.
Keep this file short, factual, and tied to discoverable patterns in the repo.
-->

# Repo-specific instructions for AI coding agents

Purpose: give an AI code agent immediate, practical context to make correct edits, CI changes, and local-run suggestions for this project.

What is known (from repository):
- CI/CD uses GitHub Actions under `.github/workflows/` (see `main_tracker.yml` and `azure-webapp.yml`).
- This is a Python web app intended to be deployed to Azure App Service (App name `TRACKER` appears in workflows).
- Workflows expect a `requirements.txt` and use virtual environments; tests run with `pytest` if present.
- Two different Python versions appear in workflows: `3.10` (older workflow) and `3.12` (main_tracker). Be conservative: target 3.10–3.12 compatibility.

Quick local developer actions (explicit, concrete):
- Linux / macOS (used by CI workflows):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest  # optional — workflows run pytest when it exists
```
- Windows PowerShell (user default shell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

CI / CD specifics agents must know:
- `main_tracker.yml` (primary):
  - Runs on `ubuntu-latest`, sets up Python `3.12`, creates and activates a venv, installs `requirements.txt` and uploads the repository (excluding `venv/`) as artifact named `python-app`.
  - Deploy step logs into Azure using service principal secrets (see secret keys used in file) and uses `azure/webapps-deploy@v3` to deploy to app-name `TRACKER`.
- `azure-webapp.yml` (older workflow):
  - Uses Python `3.10`, runs `pytest` (or skips if none found), zips repo to `release.zip`, and deploys with `azure/webapps-deploy@v2` using a publish profile secret.

Secrets and auth patterns (explicit):
- One workflow uses a service principal (secrets named like `AZUREAPPSERVICE_CLIENTID_...`, `AZUREAPPSERVICE_TENANTID_...`, `AZUREAPPSERVICE_SUBSCRIPTIONID_...`).
- The other workflow uses a `publish-profile` secret (`AZURE_WEBAPP_PUBLISH_PROFILE`).
- When changing deployment behavior, update the workflow and remind maintainers to set corresponding secrets in GitHub repo settings.

Project conventions (discoverable):
- `requirements.txt` is the canonical dependency file. Workflows assume it exists at repo root.
- Virtualenv folder name: `venv` (CI purposely excludes `venv/` during artifact upload).
- Tests: `pytest` is the expected test runner (workflows run `pytest || echo "No tests found, skipping"`).
- Packaging: older workflow creates `release.zip`; newer workflow uploads the raw tree as artifact. When adding build steps, keep artifact name `python-app` for compatibility.

Files to inspect when making changes:
- `.github/workflows/main_tracker.yml` — primary CI/CD flow and service-principal-based deploy.
- `.github/workflows/azure-webapp.yml` — alternate/legacy CI flow, creates `release.zip` and uses publish-profile.
- `requirements.txt` — must be present for CI to install deps.
- Typical code entrypoints to look for (if present): `app.py`, `main.py`, `wsgi.py`, `asgi.py`, `run.py`.

Integration points and things to avoid assuming:
- Integration: Azure App Service is the deployment target. Do NOT assume other infra (AKS, Functions) unless new IaC files appear.
- Avoid assuming a specific web framework (Flask, Django, FastAPI) — none is present in the repo. Inspect runtime entrypoint files before adding framework-specific code.
- Do not modify workflow secret names without updating project documentation and repo secrets.

When making edits an AI should perform first:
1. Search for `requirements.txt` and common entrypoints (`app.py`, `main.py`) before suggesting framework-specific changes.
2. If adding tests, use `pytest` and place tests under `tests/` so CI will pick them up.
3. If changing Python version in workflows, update both workflow files for consistency and call out the impact on runtime compatibility.

Examples (copy/paste from repo to reference):
- Deploy step (from `main_tracker.yml`): `uses: azure/webapps-deploy@v3` with `app-name: 'TRACKER'`.
- Artifact name used by both workflows: `python-app` (keep this name for compatibility with existing deploy steps).

If anything is unclear or you need to target a specific framework or runtime entrypoint, ask the maintainer to point to the application entry file (for example `app.py`), `requirements.txt`, and any runtime config (like `web.config`, `Procfile`, or `runtime.txt`).

Please review — tell me which runtime entrypoint and web framework this project uses (if known) so I can tighten framework-specific guidance.
