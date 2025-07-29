# src/{{ project_slug }}/models/item.py

from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=300, description="Optional description of the item")
    price: float = Field(..., gt=0, description="Price of the item, must be greater than 0")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: Optional[float] = Field(None, gt=0)

class ItemInDBBase(ItemBase):
    id: int = Field(..., description="Unique ID of the item")

    class Config:
        # Pydantic V1 way for ORM mode
        # orm_mode = True 
        # Pydantic V2 way for ORM mode (now called from_attributes)
        from_attributes = True

# Item model as stored in the database (could be an ORM model instance)
class Item(ItemInDBBase):
    pass

# Item model to return to client (might exclude certain fields)
class ItemPublic(ItemInDBBase):
    pass 