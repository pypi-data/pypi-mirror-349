# src/{{ project_slug }}/routers/items.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated

# Assuming your schemas are in a module like this:
from ..schemas.item import ItemCreateRequest, ItemUpdateRequest, ItemResponse, ItemListResponse
# And your models/CRUD operations might be structured elsewhere, e.g., in a 'services' or 'crud' layer
# For this example, we'll use an in-memory store.

router = APIRouter()

# In-memory database for demonstration purposes
fake_items_db = [
    {"id": 1, "name": "Foo", "description": "An optional description for Foo", "price": 50.5},
    {"id": 2, "name": "Bar", "description": "Another optional description for Bar", "price": 120.0},
    {"id": 3, "name": "Baz", "description": None, "price": 75.25},
]

# Dependency for getting current item by ID (example)
async def get_item_by_id(item_id: int) -> dict:
    item = next((item for item in fake_items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreateRequest):
    """
    Create a new item.
    """
    new_id = max(i["id"] for i in fake_items_db) + 1 if fake_items_db else 1
    new_item_data = item.model_dump()
    new_item = {"id": new_id, **new_item_data}
    fake_items_db.append(new_item)
    return new_item

@router.get("/", response_model=ItemListResponse)
async def read_items(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of items with pagination.
    """
    items_to_return = fake_items_db[skip : skip + limit]
    return {"items": items_to_return, "total": len(fake_items_db)}

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item: Annotated[dict, Depends(get_item_by_id)]):
    """
    Retrieve a single item by its ID.
    """
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_update: ItemUpdateRequest):
    """
    Update an existing item by its ID.
    """
    db_item = await get_item_by_id(item_id) # Ensure item exists
    
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        db_item[key] = value
    
    # In a real DB, you'd save the changes here.
    # For our fake DB, the db_item is a reference, so it's already updated.
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    db_item = await get_item_by_id(item_id) # Ensure item exists
    fake_items_db.remove(db_item)
    return # No content response 