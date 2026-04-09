async def test_get_users_empty(client):
    response = await client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_users(client):
    await client.post("/users/", json={
        "login": "test@test.com",
        "password": "password123",
        "project_id": "66d8047e-65a4-4d07-bf84-dff47bdcd2a6",
        "env": "prod",
        "domain": "canary"
    })  

    response = await client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["login"] == "test@test.com"


async def test_create_user(client):
    response = await client.post("/users/", json={
        "login": "test@test.com",
        "password": "password123",
        "project_id": "66d8047e-65a4-4d07-bf84-dff47bdcd2a6",
        "env": "prod",
        "domain": "canary"
    })

    assert response.status_code == 201
    assert response.json()["login"] == "test@test.com"
    assert response.json()["env"] == "prod"


async def test_lock_user(client):
    await client.post("/users/", json={
        "login": "test@test.com",
        "password": "password123",
        "project_id": "66d8047e-65a4-4d07-bf84-dff47bdcd2a6",
        "env": "prod",
        "domain": "canary"
    })  

    response = await client.post("/users/lock")
    assert response.status_code == 200


async def test_lock_user_not_found(client):
    response = await client.post("/users/lock")
    assert response.status_code == 404
    

async def test_free_users(client):
    await client.post("/users/", json={
        "login": "test@test.com",
        "password": "password123",
        "project_id": "66d8047e-65a4-4d07-bf84-dff47bdcd2a6",
        "env": "prod",
        "domain": "canary"
    })  

    response = await client.delete("/users/lock")
    assert response.status_code == 200


async def test_free_after_lock(client):
    await client.post("/users/", json={
        "login": "test@test.com",
        "password": "password123",
        "project_id": "66d8047e-65a4-4d07-bf84-dff47bdcd2a6",
        "env": "prod",
        "domain": "canary"
    })  

    lock_response = await client.post("/users/lock")
    assert lock_response.status_code == 200

    free_response = await client.delete("/users/lock")
    assert free_response.status_code == 200
