from fastapi import status


def _create_task(client, title: str = "Study SQL") -> dict:
    response = client.post("/tasks", json={"title": title})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "StudentTask API is running"}


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Study SQL"})

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Study SQL"
    assert body["completed"] is False


def test_create_task_requires_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_all_tasks_empty(client):
    response = client.get("/tasks")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_tasks_returns_created(client):
    _create_task(client, "First")
    _create_task(client, "Second")

    response = client.get("/tasks")

    assert response.status_code == status.HTTP_200_OK
    titles = [task["title"] for task in response.json()]
    assert titles == ["First", "Second"]


def test_get_task_by_id(client):
    created = _create_task(client)

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == created


def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client):
    created = _create_task(client)

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "Study SQL well", "completed": True},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["title"] == "Study SQL well"
    assert body["completed"] is True


def test_update_task_persists(client):
    created = _create_task(client)

    client.put(
        f"/tasks/{created['id']}",
        json={"title": "Updated", "completed": True},
    )
    response = client.get(f"/tasks/{created['id']}")

    body = response.json()
    assert body["title"] == "Updated"
    assert body["completed"] is True


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999",
        json={"title": "Nope", "completed": True},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client):
    created = _create_task(client)

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Task deleted successfully"}

    follow_up = client.get(f"/tasks/{created['id']}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_database_isolated_between_tests(client):
    """Each test starts from an empty database (fixture isolation)."""
    response = client.get("/tasks")

    assert response.json() == []
