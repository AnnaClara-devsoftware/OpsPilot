def test_create_and_list_projects(client, auth_headers):
    resp = client.post(
        "/api/v1/projects",
        json={"name": "Meu Projeto", "description": "desc", "source_type": "path", "source_reference": "/tmp/proj"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    project = resp.json()
    assert project["name"] == "Meu Projeto"

    resp = client.get("/api/v1/projects", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_project_not_found(client, auth_headers):
    resp = client.get("/api/v1/projects/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert resp.status_code == 404


def test_projects_require_auth(client):
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 401


def test_delete_project(client, auth_headers):
    create_resp = client.post(
        "/api/v1/projects",
        json={"name": "Del", "source_type": "path", "source_reference": "/tmp/del"},
        headers=auth_headers,
    )
    project_id = create_resp.json()["id"]
    resp = client.delete(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 204
    resp = client.get(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 404
