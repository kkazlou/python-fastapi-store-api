def test_create_store(client):
    response = client.post("/stores", json={"name": "Test Store"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Store"
    assert "id" in data


def test_create_item(client):
    response = client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data


def test_create_tag(client):
    response = client.post("/tags", json={"name": "Test Tag"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Tag"
    assert "id" in data


def test_get_stores(client):
    # Create test store first
    client.post("/stores", json={"name": "Test Store"})

    response = client.get("/stores")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Store"


def test_add_item_to_store(client):
    # Create store and item
    store_response = client.post("/stores", json={"name": "Test Store"})
    store_id = store_response.json()["id"]

    item_response = client.post("/items", json={"name": "Test Item"})
    item_id = item_response.json()["id"]

    # Add item to store
    response = client.post(f"/stores/{store_id}/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Test Item"


def test_add_tag_to_item(client):
    # Create item and tag
    item_response = client.post("/items", json={"name": "Test Item"})
    item_id = item_response.json()["id"]

    tag_response = client.post("/tags", json={"name": "Test Tag"})
    tag_id = tag_response.json()["id"]

    # Add tag to item
    response = client.post(f"/items/{item_id}/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "Test Tag"


def test_update_store(client):
    # Create store
    response = client.post("/stores", json={"name": "Test Store"})
    store_id = response.json()["id"]

    # Update store
    response = client.put(f"/stores/{store_id}", json={"name": "Updated Store"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Store"


def test_delete_store(client):
    # Create store
    response = client.post("/stores", json={"name": "Test Store"})
    store_id = response.json()["id"]

    # Delete store
    response = client.delete(f"/stores/{store_id}")
    assert response.status_code == 200

    # Verify store is deleted
    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 404


def test_remove_item_from_store(client):
    # Create store and item
    store_response = client.post("/stores", json={"name": "Test Store"})
    store_id = store_response.json()["id"]

    item_response = client.post("/items", json={"name": "Test Item"})
    item_id = item_response.json()["id"]

    # Add item to store
    client.post(f"/stores/{store_id}/items/{item_id}")

    # Remove item from store
    response = client.delete(f"/stores/{store_id}/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0


def test_remove_tag_from_item(client):
    # Create item and tag
    item_response = client.post("/items", json={"name": "Test Item"})
    item_id = item_response.json()["id"]

    tag_response = client.post("/tags", json={"name": "Test Tag"})
    tag_id = tag_response.json()["id"]

    # Add tag to item
    client.post(f"/items/{item_id}/tags/{tag_id}")

    # Remove tag from item
    response = client.delete(f"/items/{item_id}/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 0
