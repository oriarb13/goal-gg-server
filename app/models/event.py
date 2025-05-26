from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import SportCategoryEnum, EventStatusEnum

class Event(Base):
    __tablename__ = "events"
    
    # Basic info
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    image = Column(String, default="default-event.jpg")
    
    # Relations
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    club = relationship("Club", back_populates="events")
    field_id = Column(Integer) 
    
    # Location
    location = Column(JSON, nullable=False)  # {"address": "...", "lat": 32.0, "lng": 34.0}
    
    # Time
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # Teams (key-value pairs)
    teams = Column(JSON, default={})  # {"a": [19,22,31], "b": [40,50,26]}
    
    # Settings
    sport_category = Column(ENUM(SportCategoryEnum), nullable=False)
    status = Column(ENUM(EventStatusEnum), default=EventStatusEnum.UPCOMING)  # upcoming/full/ongoing/completed
    max_participants = Column(Integer, default=50)
    min_participants_to_start = Column(Integer, default=5)
    cost = Column(Float, default=0.0)
    
    # Relations
    games = relationship("Game", back_populates="event")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())