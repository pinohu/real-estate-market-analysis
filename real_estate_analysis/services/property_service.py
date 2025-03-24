"""
Property service module.
Handles business logic for property management.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.models import Property, User
from ..models.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException, status

class PropertyService:
    def __init__(self, db: Session):
        self.db = db

    def get_properties(
        self,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None
    ) -> List[Property]:
        """Get list of properties with optional filtering."""
        query = self.db.query(Property)
        if owner_id:
            query = query.filter(Property.owner_id == owner_id)
        return query.offset(skip).limit(limit).all()

    def get_property(self, property_id: int) -> Optional[Property]:
        """Get a specific property by ID."""
        return self.db.query(Property).filter(Property.id == property_id).first()

    def create_property(
        self,
        property: PropertyCreate,
        owner_id: int
    ) -> Property:
        """Create a new property."""
        db_property = Property(
            **property.dict(),
            owner_id=owner_id
        )
        self.db.add(db_property)
        self.db.commit()
        self.db.refresh(db_property)
        return db_property

    def update_property(
        self,
        property_id: int,
        property: PropertyUpdate,
        owner_id: int
    ) -> Property:
        """Update a property."""
        db_property = self.get_property(property_id)
        if not db_property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        if db_property.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        update_data = property.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_property, field, value)

        self.db.commit()
        self.db.refresh(db_property)
        return db_property

    def delete_property(self, property_id: int, owner_id: int) -> bool:
        """Delete a property."""
        db_property = self.get_property(property_id)
        if not db_property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        if db_property.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        self.db.delete(db_property)
        self.db.commit()
        return True 