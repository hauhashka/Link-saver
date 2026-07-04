from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_link():
    with TestClient(app) as client:
        response = client.post(
            "/links",
            json={
                "title": "FastAPI Docs",
                "url": "https://fastapi.tiangolo.com",
                "description": "Official FastAPI documentation",
                "is_favorite": True,
            },
        )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "FastAPI Docs"
    assert data["description"] == "Official FastAPI documentation"
    assert data["is_favorite"] is True
    assert "id" in data


def test_get_links():
    with TestClient(app) as client:
        response = client.get("/links")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_get_one_link():
    with TestClient(app) as client:
        create_response = client.post(
            "/links",
            json={
                "title": "Python Docs",
                "url": "https://docs.python.org/3/",
                "description": "Official Python documentation",
                "is_favorite": False,
            },
        )

        created_link = create_response.json()
        link_id = created_link["id"]

        get_response = client.get(f"/links/{link_id}")

    data = get_response.json()

    assert get_response.status_code == 200
    assert data["id"] == link_id
    assert data["title"] == "Python Docs"


def test_create_and_update_link():
    with TestClient(app) as client:
        create_response = client.post(
            "/links",
            json={
                "title": "Old Title",
                "url": "https://example.com",
                "description": "Old description",
                "is_favorite": False,
            },
        )

        created_link = create_response.json()
        link_id = created_link["id"]

        update_response = client.put(
            f"/links/{link_id}",
            json={
                "title": "New Title",
                "url": "https://example.com",
                "description": "New description",
                "is_favorite": True,
            },
        )

    data = update_response.json()

    assert update_response.status_code == 200
    assert data["id"] == link_id
    assert data["title"] == "New Title"
    assert data["description"] == "New description"
    assert data["is_favorite"] is True


def test_create_and_delete_link():
    with TestClient(app) as client:
        create_response = client.post(
            "/links",
            json={
                "title": "Delete Me",
                "url": "https://example.com",
                "description": "This link should be deleted",
                "is_favorite": False,
            },
        )

        created_link = create_response.json()
        link_id = created_link["id"]

        delete_response = client.delete(f"/links/{link_id}")
        get_response = client.get(f"/links/{link_id}")

    assert delete_response.status_code == 200
    assert get_response.status_code == 404


def test_search_links():
    with TestClient(app) as client:
        client.post(
            "/links",
            json={
                "title": "SQLModel Tutorial",
                "url": "https://sqlmodel.tiangolo.com",
                "description": "Python SQL toolkit",
                "is_favorite": True,
            },
        )

        response = client.get("/links?search=sqlmodel")

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(link["title"] == "SQLModel Tutorial" for link in data)


def test_filter_favorite_links():
    with TestClient(app) as client:
        client.post(
            "/links",
            json={
                "title": "Favorite Link",
                "url": "https://example.com/favorite",
                "description": "Favorite test link",
                "is_favorite": True,
            },
        )

        response = client.get("/links?favorite=true")

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(link["is_favorite"] is True for link in data)