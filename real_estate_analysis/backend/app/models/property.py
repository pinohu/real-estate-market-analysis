from sqlalchemy import Boolean, Column, Integer, String, DateTime, Numeric, ForeignKey, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    square_feet = Column(Numeric(10, 2))
    property_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    year_built = Column(Integer)
    lot_size = Column(Numeric(10, 2))
    features = Column(ARRAY(String))
    images = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="properties")
    analyses = relationship("Analysis", back_populates="property") 