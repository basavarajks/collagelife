def test_health_endpoint(client):
    response = client.get("/api/v1/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_login_validation(client):
    response = client.post("/api/v1/auth/login", json={})
    assert response.status_code == 400
    assert "required" in response.get_json()["error"]["message"]


def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={"user_id": "student1", "password": "wrongpass"})
    assert response.status_code == 401


def test_login_and_protected_route(client):
    login = client.post("/api/v1/auth/login", json={"user_id": "student1", "password": "pass1234"})
    assert login.status_code == 200

    token = login.get_json()["data"]["token"]
    protected = client.get("/api/v1/api/protected", headers={"Authorization": "Bearer " + token})
    assert protected.status_code == 200
    assert protected.get_json()["data"]["role"] == "Student"


def test_protected_requires_auth(client):
    response = client.get("/api/v1/api/protected")
    assert response.status_code == 401
