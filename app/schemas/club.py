from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.enums import SportCategoryEnum, ClubStatusEnum

# Create Club
class ClubCreate(BaseModel):
   name: str
   description: str
   image: Optional[str] = "default-club.jpg"
   admin_id: int
   sport_category: SportCategoryEnum
   is_private: Optional[bool] = False
   max_players: int
   status: Optional[ClubStatusEnum] = ClubStatusEnum.ACTIVE
   location: dict

# Full Club
class ClubFull(BaseModel):
   id: int
   name: str
   description: str
   image: str
   admin_id: int
   captains: List[int]
   sport_category: SportCategoryEnum
   is_private: bool
   max_players: int
   status: ClubStatusEnum
   location: dict
   pending_requests: List[int]
   created_at: datetime
   updated_at: Optional[datetime]
   
   class Config:
       from_attributes = True