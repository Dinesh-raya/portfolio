# GitHub Trending Data Pipeline

Daily ETL pipeline that tracks trending GitHub repos and visualizes trends.

## How it works

1. **Extract** — GitHub Search API finds top repos (sorted by stars)
2. **Transform** — Clean, normalize, structure with pandas
3. **Load** — Store in SQLite (repo_snapshots + daily_summary tables)
4. **Schedule** — GitHub Actions cron runs daily at 06:00 UTC
5. **Dashboard** — Streamlit app shows trends, top repos, language distribution

## Run locally

```bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run dashboard/app.py
```

## Deploy dashboard on Streamlit Cloud

1. Push to GitHub
2. [Streamlit Cloud](https://streamlit.io/cloud) → New app → select `projects/data-pipeline/dashboard/app.py`
3. Deploy (no secrets needed)

## Pipeline schedule

The `.github/workflows/pipeline.yml` runs daily and auto-commits the updated database. GitHub Actions gives 2,000 free minutes/month — more than enough for a daily 1-minute job.

## Stack

| Layer | Tool |
|-------|------|
| Source | GitHub API (free, no key) |
| Transform | pandas |
| Storage | SQLite |
| Schedule | GitHub Actions cron |
| Dashboard | Streamlit + Plotly |