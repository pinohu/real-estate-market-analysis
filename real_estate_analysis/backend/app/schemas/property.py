from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    price: Decimal
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[Decimal] = None
    property_type: str
    status: str
    year_built: Optional[int] = None
    lot_size: Optional[Decimal] = None
    features: Optional[List[str]] = None
    images: Optional[List[str]] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    title: Optional[str] = None
    price: Optional[Decimal] = None
    status: Optional[str] = None

class PropertyInDBBase(PropertyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Property(PropertyInDBBase):
    pass

class PropertyResponse(PropertyInDBBase):
    pass 