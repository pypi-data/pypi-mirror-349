# tests/test_items_api.py

import pytest
from httpx import AsyncClient
from fastapi import status

# Assuming your ItemResponse schema is defined and accessible
# from {{ project_slug }}.schemas.item import ItemResponse 

@pytest.mark.asyncio
async def test_read_root(test_client: AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert "{{ project_name }}" in response.json()["message"]

@pytest.mark.asyncio
async def test_create_item(test_client: AsyncClient):
    item_data = {"name": "Test Item", "description": "A test item", "price": 99.99}
    response = await test_client.post("/api/v1/items/", json=item_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_item = response.json()
    assert created_item["name"] == item_data["name"]
    assert created_item["description"] == item_data["description"]
    assert created_item["price"] == item_data["price"]
    assert "id" in created_item
    # Store the ID for subsequent tests if needed, or ensure teardown
    # pytest.created_item_id = created_item["id"] # Example of sharing state (use with caution)

@pytest.mark.asyncio
async def test_read_items(test_client: AsyncClient):
    # First, create an item to ensure there's at least one
    await test_client.post("/api/v1/items/", json={"name": "Item for Listing", "price": 10.0})
    
    response = await test_client.get("/api/v1/items/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0 # Assuming the created item is listed

@pytest.mark.asyncio
async def test_read_specific_item(test_client: AsyncClient):
    # Create an item first to ensure it exists
    item_payload = {"name": "Specific Item", "description": "Details here", "price": 25.50}
    create_response = await test_client.post("/api/v1/items/", json=item_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    item_id = create_response.json()["id"]

    response = await test_client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == status.HTTP_200_OK
    item = response.json()
    assert item["id"] == item_id
    assert item["name"] == item_payload["name"]

@pytest.mark.asyncio
async def test_read_nonexistent_item(test_client: AsyncClient):
    response = await test_client.get("/api/v1/items/999999") # Assuming this ID won't exist
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_update_item(test_client: AsyncClient):
    # Create an item first
    item_payload = {"name": "Item to Update", "price": 30.0}
    create_response = await test_client.post("/api/v1/items/", json=item_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    item_id = create_response.json()["id"]

    update_payload = {"name": "Updated Item Name", "price": 35.50, "description": "Now with description"}
    response = await test_client.put(f"/api/v1/items/{item_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    updated_item = response.json()
    assert updated_item["id"] == item_id
    assert updated_item["name"] == update_payload["name"]
    assert updated_item["price"] == update_payload["price"]
    assert updated_item["description"] == update_payload["description"]

@pytest.mark.asyncio
async def test_delete_item(test_client: AsyncClient):
    # Create an item first
    item_payload = {"name": "Item to Delete", "price": 40.0}
    create_response = await test_client.post("/api/v1/items/", json=item_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    item_id = create_response.json()["id"]

    delete_response = await test_client.delete(f"/api/v1/items/{item_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's gone
    get_response = await test_client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 