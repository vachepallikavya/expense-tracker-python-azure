# Expense Tracker (Flask) with GitHub Actions → Azure App Service

A tiny personal expense tracker built with Flask + SQLite. CI/CD uses GitHub Actions to deploy to **Azure App Service (Linux)**.

---

## 0) Prerequisites
- Python 3.12+ installed
- Git + GitHub account
- Azure subscription
- (Optional) Azure CLI installed

## 1) Run Locally
```bash
git clone <your-repo-url> expense-tracker
cd expense-tracker

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

# create your .env
cp .env.example .env
# edit .env and set FLASK_SECRET_KEY (any random string)

# initialize local DB
python -m flask --app app init-db

# start app
python -m flask --app app run
# open http://127.0.0.1:5000
```

## 2) Create Azure App Service (Linux)
Portal path: **Create a resource → Web App**
- **Publish**: Code
- **Runtime stack**: Python 3.12
- **Operating System**: Linux
- **Region**: your choice
- **App name**: e.g. `exp-tracker-app` (must be globally unique)
- Finish the wizard to create the app.

### App Settings
In your App Service → **Settings → Configuration → Application settings** add:
- `FLASK_SECRET_KEY` = some-long-random-value
- `DATABASE_URL` = `sqlite:////home/data/expenses.db`
- `WEBSITES_PORT` = `8000` (optional for some stacks)
- **Startup Command** = `gunicorn -w 2 -b 0.0.0.0:8000 app:app`

Click **Save** and let the app restart.

> Why `DATABASE_URL`? On Azure we want SQLite stored under `/home`, which is the persistent volume for App Service containers. `/home/data/expenses.db` survives restarts and deployments.

## 3) Connect GitHub → Add Publish Profile Secret
In App Service → **Overview**, click **Get publish profile** to download `*.PublishSettings` XML.

In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**:
- Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
- Value: paste the entire publish profile XML

## 4) Push Code & Trigger CI/CD
Make sure your workflow file exists at `.github/workflows/azure-webapp.yml`.
Push / merge to the `main` branch to deploy.

```bash
git init
git remote add origin <your-repo-url>
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

GitHub Actions will build an artifact (`release.zip`) and deploy it to your Web App.

## 5) Initialize the DB on Azure (first time)
Open **App Service → Development Tools → SSH** (console) and run:
```bash
python -m flask --app app init-db
```
You should see `Database initialized` once. Visit your site URL to use the app.

## 6) Common Pitfalls / Fixes
- **App fails to start**: Check **Log stream** in App Service to read errors.
- **DB not saving**: Ensure `DATABASE_URL=sqlite:////home/data/expenses.db` is set in Configuration.
- **403/500 after deploy**: Make sure `Startup Command` uses `gunicorn app:app` and your `requirements.txt` includes `gunicorn`.
- **Changes not showing**: Confirm you pushed to `main` and the workflow ran successfully.

## 7) Optional: Use Postgres instead of SQLite
- Create **Azure Database for PostgreSQL - Flexible Server**.
- Set `DATABASE_URL` as `postgresql+psycopg2://<user>:<pass>@<host>:5432/<db>`
- Add `psycopg2-binary` to `requirements.txt` and redeploy.
- Run `python -m flask --app app init-db` again on Azure to create tables.

---

**Local dev tips**
- Re-run `python -m flask --app app init-db` if you change models.
- Use `FLASK_ENV=development` in `.env` to auto-reload locally.
