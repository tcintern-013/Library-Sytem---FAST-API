from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_read_book():
    response = client.post(
        "/books",
        json={"id": 101, "title": "Test Book", "author": "Tester"},
    )
    assert response.status_code == 201

    response = client.get("/books/101")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Tester"
