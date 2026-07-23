from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_signup_login_and_protected_route():
    signup_response = client.post(
        "/signup",
        json={"username": "alice", "password": "secret123"},
    )

    assert signup_response.status_code == 201
    assert signup_response.json()["message"] == "User created successfully"

    login_response = client.post(
        "/login",
        json={"username": "alice", "password": "secret123"},
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    token = login_response.json()["access_token"]
    protected_response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert protected_response.status_code == 200
    assert protected_response.json()["username"] == "alice"


def test_missing_token_is_rejected():
    response = client.get("/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
