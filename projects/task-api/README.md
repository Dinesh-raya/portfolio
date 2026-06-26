# Task Manager API

Full-featured REST API with JWT authentication and a Streamlit frontend.

## Stack

| Layer | Tech |
|-------|------|
| API | FastAPI |
| Auth | JWT (bcrypt + PyJWT) |
| Database | SQLAlchemy + SQLite |
| Frontend | Streamlit |
| Tests | pytest + httpx |
| CI | GitHub Actions |
| Deployment | Docker / Render / Hugging Face Spaces |

## Run locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
# API at http://localhost:8000, docs at http://localhost:8000/docs
streamlit run frontend/app.py
# Frontend at http://localhost:8501
```

## Run with Docker

```bash
docker-compose up --build
# API at http://localhost:8000, frontend at http://localhost:8501
```

## Test

```bash
pytest -v
```

## Deploy

### API on Render (free)

1. Push to GitHub
2. [Render](https://render.com) → New Web Service → connect repo
3. Root directory: `projects/task-api`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn api.main:app --host 0.0.0.0 --port 10000`
6. Set `PYTHON_VERSION=3.12` in env

### Frontend on Streamlit Cloud (free)

1. [Streamlit Cloud](https://streamlit.io/cloud) → New app
2. Path: `projects/task-api/frontend/app.py`
3. Add secret: `API_URL=https://your-render-url.onrender.com`

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Get JWT token |
| GET | `/tasks` | Yes | List your tasks |
| POST | `/tasks` | Yes | Create task |
| GET | `/tasks/{id}` | Yes | Get task |
| PATCH | `/tasks/{id}` | Yes | Update task |
| DELETE | `/tasks/{id}` | Yes | Delete task |
