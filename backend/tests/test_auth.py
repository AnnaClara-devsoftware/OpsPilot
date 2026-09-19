def test_register_and_login(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "ana@example.com", "full_name": "Ana Clara", "password": "supersecret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "ana@example.com"
    assert "id" in data

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "supersecret123"},
    )
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_register_duplicate_email_fails(client):
    payload = {"email": "dup@example.com", "full_name": "Dup", "password": "supersecret123"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wp@example.com", "full_name": "WP", "password": "supersecret123"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": "wp@example.com", "password": "wrongpass"})
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_me_with_token(client, auth_headers):
    resp = client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@example.com"


def test_refresh_token_flow(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "ref@example.com", "full_name": "Ref", "password": "supersecret123"},
    )
    login_resp = client.post("/api/v1/auth/login", json={"email": "ref@example.com", "password": "supersecret123"})
    refresh_token = login_resp.json()["refresh_token"]

    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
