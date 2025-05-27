from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import SportCategoryEnum, ClubStatusEnum

class Club(Base):
    __tablename__ = "clubs"
    
    # Basic info
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    image = Column(String, default="default-club.jpg")
    
    # Admin & Captains
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    admin = relationship("User", foreign_keys=[admin_id],back_populates="owned_clubs")
    captains_ids = Column(ARRAY(Integer),ForeignKey("members.id"), default=[])  # IDs of captains as members
    captains = relationship("Member", foreign_keys=[captains_ids])
    # Sport
    sport_category = Column(ENUM(SportCategoryEnum), nullable=False)
    
    # Settings
    is_private = Column(Boolean, default=False)
    max_players = Column(Integer, nullable=False)
    status = Column(ENUM(ClubStatusEnum), default=ClubStatusEnum.ACTIVE)
    
    # Location
    location = Column(JSON, default={
        "country": None,
        "city": None, 
        "address": None,
        "lat": None,
        "lng": None
    })
    
    # Members & Requests (JSON arrays)
    members = relationship("Member", back_populates="club")
    pending_requests = Column(ARRAY(Integer), default=[])  
    
    #events
    events = relationship("Event", back_populates="club")

    # Timestamps    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())