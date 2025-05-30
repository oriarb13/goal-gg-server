from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from app.models.enums import SportCategoryEnum, ClubStatusEnum

class Location(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    class Config:
        from_attributes = True

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
    status: Optional[ClubStatusEnum] = ClubStatusEnum.ACTIVE
    location: Location

# Full Club
class ClubFull(BaseModel):
    id: int
    name: str
    description: str
    image: str
    admin_id: int
    admin: Optional[UserInfo] = None  # admin info
    captains_ids: Optional[List[int]] = []  
    captains: Optional[List[MemberInfo]] = []  # captains info
    sport_category: SportCategoryEnum
    is_private: bool
    max_players: int
    status: Optional[ClubStatusEnum] = None
    location: Optional[Dict] = None
    pending_requests: Optional[List[int]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    members: Optional[List[MemberInfo]] = []  # members info
    
    class Config:
        from_attributes = True

#for single club page
class clubById(BaseModel):
    id: int
    name: str
    description: str
    image: str
    admin_id: int
    admin: Optional[UserInfo] = None  # admin info
    captains_ids: Optional[List[int]] = []  
    captains: Optional[List[MemberInfo]] = []  # captains info
    sport_category: SportCategoryEnum
    is_private: bool
    max_players: int
    status: Optional[ClubStatusEnum] = None
    location: Optional[Dict] = None
    pending_requests: Optional[List[int]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    members: Optional[List[MemberInfo]] = []  # members info
    
    class Config:
        from_attributes = True

