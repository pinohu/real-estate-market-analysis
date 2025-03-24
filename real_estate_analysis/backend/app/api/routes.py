from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..core.database import get_db
from ..models.user import User
from ..services.auth import get_current_user
from ..schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from ..schemas.analysis import AnalysisRequest, AnalysisResponse
from ..services.property import (
    create_property,
    get_property,
    get_properties,
    update_property,
    delete_property,
    analyze_property,
    analyze_market
)

router = APIRouter()

@router.post("/properties", response_model=PropertyResponse)
def create_new_property(
    property: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new property.
    """
    return create_property(db=db, property=property, user_id=current_user.id)

@router.get("/properties", response_model=List[PropertyResponse])
def read_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve properties.
    """
    return get_properties(db=db, skip=skip, limit=limit, user_id=current_user.id)

@router.get("/properties/{property_id}", response_model=PropertyResponse)
def read_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get property by ID.
    """
    property = get_property(db=db, property_id=property_id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property_info(
    property_id: int,
    property: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update property information.
    """
    updated_property = update_property(
        db=db, property_id=property_id, property=property, user_id=current_user.id
    )
    if not updated_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated_property

@router.delete("/properties/{property_id}")
def delete_property_info(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete property.
    """
    deleted = delete_property(db=db, property_id=property_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted successfully"}

@router.post("/properties/{property_id}/analyze", response_model=AnalysisResponse)
def analyze_property_endpoint(
    property_id: int,
    analysis_request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Analyze a property.
    """
    analysis = analyze_property(
        db=db,
        property_id=property_id,
        analysis_request=analysis_request,
        user_id=current_user.id
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Property not found")
    return analysis

@router.post("/market/analyze", response_model=AnalysisResponse)
def analyze_market_endpoint(
    analysis_request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Analyze market conditions.
    """
    return analyze_market(db=db, analysis_request=analysis_request, user_id=current_user.id) 