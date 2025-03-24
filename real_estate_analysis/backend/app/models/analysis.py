from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, JSON, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analysis_type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metrics = Column(JSON)
    insights = Column(ARRAY(String))
    recommendations = Column(ARRAY(String))
    market_metrics = Column(JSON)
    property_metrics = Column(JSON)
    confidence_score = Column(Numeric(5, 2))
    data_sources = Column(ARRAY(String))
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    property = relationship("Property", back_populates="analyses")
    user = relationship("User", back_populates="analyses") 