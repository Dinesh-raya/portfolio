from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200

def test_register_login():
    r = client.post("/auth/register", json={"username": "testuser", "password": "test123"})
    assert r.status_code == 200
    token = r.json()["token"]
    assert token

    r = client.post("/auth/login", json={"username": "testuser", "password": "test123"})
    assert r.status_code == 200

def test_crud():
    r = client.post("/auth/register", json={"username": "crudtest", "password": "test123"})
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/tasks", json={"title": "My task"}, headers=headers)
    assert r.status_code == 201
    task_id = r.json()["id"]

    r = client.get("/tasks", headers=headers)
    assert len(r.json()) == 1

    r = client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=headers)
    assert r.json()["completed"] is True

    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 204
