# src/{{ project_slug }}/schemas/item.py

# This file is for Pydantic schemas used in API requests and responses.
# They might be identical to your models, or they might be a subset
# or superset, or have different validation rules for API interaction.

# For simplicity, we can re-export models if schemas are identical,
# or define specific request/response schemas here.

from typing import List, Optional
from pydantic import BaseModel
from ..models.item import ItemBase, ItemInDBBase # Import base models

# Schema for creating an item (request body for POST)
class ItemCreateRequest(ItemBase):
    pass

# Schema for updating an item (request body for PUT/PATCH)
class ItemUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Schema for an individual item response
class ItemResponse(ItemInDBBase):
    pass

# Schema for a list of items in response
class ItemListResponse(BaseModel):
    items: List[ItemResponse]
    total: int 