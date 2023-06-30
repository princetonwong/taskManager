from fastapi.testclient import TestClient
from app.app import app
from uuid import UUID
from app.database import Database

client = TestClient(app)


def test_read_tasks():
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200


def test_create_task():
    sample_payload = {"name": "Test Task",
                      "description": "Test Description",
                      "done": True,
                      "created_by": "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6b",
                      "updated_by": "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6b",
                      }
    response = client.post("/api/v1/tasks/", json=sample_payload)
    assert response.status_code == 201
    assert type(UUID(response.json()["id"])) == UUID
    assert response.json()["name"] == "Test Task"
    assert response.json()["description"] == "Test Description"
    assert response.json()["done"] is True
    assert response.json()["created_by"] == "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6b"
    assert response.json()["updated_by"] == "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6b"
    client.uid = response.json()["id"]


def test_read_task():
    response = client.get(f"/api/v1/tasks/{client.uid}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Task"
    assert response.json()["description"] == "Test Description"


def test_update_task():
    sample_payload = {"name": "Test Task Updated",
                      "description": "Test Description Updated",
                      "updated_by": "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6c",
                      }
    response = client.patch(f"/api/v1/tasks/{client.uid}", json=sample_payload)
    assert response.status_code == 202
    assert response.json()["name"] == "Test Task Updated"
    assert response.json()["description"] == "Test Description Updated"
    assert response.json()["updated_by"] == "d0e3d3e0-0b7e-4b1e-8b7a-5b0b6b9b0b6c"


def test_delete_task():
    from app.model.taskModel import Task
    response = client.delete(f"/api/v1/tasks/{client.uid}")
    assert response.status_code == 200
    assert response.json()["Message"] == "Task deleted successfully"
    assert Database().session.get(Task, client.uid) is None
