from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_review_empty():
    r = client.post("/review", json={"code": "", "language": "python", "focus": "all"})
    assert r.status_code == 400

def test_review_invalid_focus():
    r = client.post("/review", json={"code": "x = 1", "language": "python", "focus": "invalid"})
    assert r.status_code == 400

def test_review_success():
    code = "def add(a, b):\n    return a + b"
    r = client.post("/review", json={"code": code, "language": "python", "focus": "style"})
    if r.status_code == 200:
        data = r.json()
        assert data["line_count"] == 2
        assert data["language"] == "python"
        assert data["focus"] == "style"
        assert len(data["feedback"]) > 0
