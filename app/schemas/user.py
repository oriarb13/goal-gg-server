from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from app.models.enums import SportCategoryEnum, StrongSideEnum, AccountStatusEnum

class RoleInfo(BaseModel):
    id: int
    name: str
    max_clubs: int
    max_players: int
    cost: float
    class Config:
        from_attributes = True


# Club info 
class OwnedClubInfo(BaseModel):
    id: int
    name: str
    description: str
    sport_category: SportCategoryEnum
    max_players: int
    
    class Config:
        from_attributes = True


class MembershipInfo(BaseModel):
    id: int
    club_id: int
    club: OwnedClubInfo
    total_goals: int
    total_assists: int
    total_games: int
    skill_rating: Optional[float]
    positions: List[str]
    
    class Config:
        from_attributes = True

# Create
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: Dict[str, str]       
    email: EmailStr
    password: str
    sport_category: SportCategoryEnum
    year_of_birth: int
    country: Optional[str] = None
    city: Optional[str] = None

# Login 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserFull(BaseModel):
    # Basic info
    id: int
    first_name: str
    last_name: str
    image: str
    year_of_birth: int

    # Relationships
    memberships: List[MembershipInfo] = []
    owned_clubs: List[OwnedClubInfo] = []
    
    # Contact info
    email: str
    is_email_verified: bool
    phone: Dict[str, str]
    city: Optional[str]
    country: Optional[str]
    
    # Sport info
    sport_category: SportCategoryEnum
    positions: List[str]
    cm: Optional[int]
    kg: Optional[int]
    strong_side: Optional[StrongSideEnum]
    avg_skill_rating: float
    
    # Auth
    account_status: AccountStatusEnum
    
    # Location
    location: Dict[str, Optional[float]]  # {"lat": None, "lng": None}
    
    # IDs of connections
    favorite_fields: List[int]
    friends: List[int]
    friend_requests: List[int]
    club_requests: List[int]
    
    # Stats
    total_games: int
    total_points: int
    total_assists: int
    
    # Role & Subscription
    role_id: int
    role: RoleInfo
    subscription_start_date: Optional[datetime]
    subscription_end_date: Optional[datetime]
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

