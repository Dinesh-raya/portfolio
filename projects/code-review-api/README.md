# AI Code Review API

Submit code via API and get an AI-powered review — bugs, security, style, and performance. Powered by Google Gemini (free tier).

## Stack

| Layer | Tech |
|-------|------|
| API | FastAPI |
| AI | Google Gemini 2.5 Flash (free) |
| Frontend | Streamlit |
| Tests | pytest + httpx |
| CI | GitHub Actions |
| Deployment | Docker / Render |

## Run locally

```bash
export GEMINI_API_KEY=your_key
pip install -r requirements.txt
uvicorn api.main:app --reload
# API at http://localhost:8000, docs at http://localhost:8000/docs
```

## Frontend

```bash
streamlit run frontend/app.py
```

## API

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a,b): return a+b", "language": "python", "focus": "all"}'
```

## Deploy

### API on Render (free)

1. Push to GitHub
2. [Render](https://render.com) → New Web Service → connect repo
3. Root directory: `projects/code-review-api`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn api.main:app --host 0.0.0.0 --port 10000`
6. Add env var `GEMINI_API_KEY`

### Frontend on Streamlit Cloud (free)

1. [Streamlit Cloud](https://streamlit.io/cloud) → New app
2. Path: `projects/code-review-api/frontend/app.py`
3. Add secret: `API_URL = "https://your-render-url.onrender.com"`

## Get a free Gemini key

https://aistudio.google.com/apikey — no credit card needed.
