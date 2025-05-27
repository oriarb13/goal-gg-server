from sqlalchemy import Column, Integer, Float, ARRAY, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import ForeignKey
from app.models.enums import FootballPositionsEnum
from sqlalchemy.dialects.postgresql import ENUM
class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    club = relationship("Club", back_populates="members")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="memberships")
    #stats
    total_goals = Column(Integer, default=0)
    total_assists = Column(Integer, default=0) 
    total_games = Column(Integer, default=0)
    skill_rating = Column(Float)
    positions = Column(ARRAY(String)) 
    #timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
