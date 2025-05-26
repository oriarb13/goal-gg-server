from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM, JSON
import datetime
# from geoalchemy2 import Geography #for location

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import (
   UserRoleEnum, SportCategoryEnum, StrongSideEnum, 
   AccountStatusEnum, FootballPositionsEnum, BasketballPositionsEnum
)

class User(Base):
   __tablename__ = "users"
   
   # Basic info
   id = Column(Integer, primary_key=True, index=True)
   first_name = Column(String(12), nullable=False)
   last_name = Column(String(12), nullable=False)
   image = Column(String, default="default-profile.jpg")
   year_of_birth = Column(Integer, nullable=False)
   
   # Contact info
   email = Column(String, unique=True, index=True, nullable=False)
   is_email_verified = Column(Boolean, default=False)
   phone = Column(JSON, default={"prefix": None, "number": None})

   city = Column(String(30))
   country = Column(String(30))
   
   # Sport info
   sport_category = Column(ENUM(SportCategoryEnum), nullable=False)
   positions = Column(ARRAY(String), default=[])  #list of positions
   cm = Column(Integer)  #height
   kg = Column(Integer)  #weight
   strong_side = Column(ENUM(StrongSideEnum))
   avg_skill_rating = Column(Float, default=0.0)
   
   # Auth
   password = Column(String, nullable=False)  # hashed password
   account_status = Column(ENUM(AccountStatusEnum), default=AccountStatusEnum.ACTIVE)
   
   # location = Column(Geography('POINT'))
   location = Column(JSON, default={"lat": None, "lng": None})

   
   # IDs of connections (instead of ObjectId)
   favorite_fields = Column(ARRAY(Integer), default=[])
   friends = Column(ARRAY(Integer), default=[])
   friend_requests = Column(ARRAY(Integer), default=[])
   memberships = relationship("Member", back_populates="user")
   club_requests = Column(ARRAY(Integer), default=[])
   
   # Stats
   total_games = Column(Integer, default=0)
   total_points = Column(Integer, default=0)
   total_assists = Column(Integer, default=0)
   
   # Role & Subscription
   role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
   role = relationship("Role", back_populates="users")
   owned_clubs = relationship("Club", foreign_keys="Club.admin_id", back_populates="admin")
   subscription_start_date = Column(DateTime)
   subscription_end_date = Column(DateTime)
   

   # Timestamps
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())