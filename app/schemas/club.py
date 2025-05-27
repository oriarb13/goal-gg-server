from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from app.models.enums import SportCategoryEnum, ClubStatusEnum

class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    image: str
    email: str
    phone: Dict[str, str]  
    
    class Config:
        from_attributes = True

class MemberInfo(BaseModel):
    id: int
    user_id: int
    user: UserInfo  
    total_goals: int
    total_assists: int
    total_games: int
    skill_rating: Optional[float] = None
    positions: List[str]
    
    class Config:
        from_attributes = True

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
    admin: UserInfo  # admin info
    captains: List[int]  
    captains_info: List[UserInfo] = []  # captains info
    sport_category: SportCategoryEnum
    is_private: bool
    max_players: int
    status: ClubStatusEnum
    location: Dict
    pending_requests: List[int]
    created_at: datetime
    updated_at: Optional[datetime]
    members: List[MemberInfo] = []  # members info
    
    class Config:
        from_attributes = True
