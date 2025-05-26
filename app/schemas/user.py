from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from app.models.enums import SportCategoryEnum, StrongSideEnum, AccountStatusEnum

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

# Full User
class UserFull(BaseModel):
    id: int
    first_name: str
    last_name: str
    image: str
    year_of_birth: int
    email: str
    is_email_verified: bool
    phone: Dict[str, str]
    city: Optional[str]
    country: Optional[str]
    sport_category: SportCategoryEnum
    positions: List[str]
    cm: Optional[int]
    kg: Optional[int]
    strong_side: Optional[StrongSideEnum]
    avg_skill_rating: float
    account_status: AccountStatusEnum
    location: dict
    
    favorite_fields: List[int]
    friends: List[int]
    friend_requests: List[int]
    clubs: List[int]
    club_requests: List[int]
    
    total_games: int
    total_points: int
    total_assists: int
    
    role_id: int
    subscription_start_date: Optional[datetime]
    subscription_end_date: Optional[datetime]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True