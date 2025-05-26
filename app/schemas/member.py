# schemas/member.py
from pydantic import BaseModel
from typing import Optional, List

# Create Member
class MemberCreate(BaseModel):
   club_id: int
   user_id: int
   total_goals: Optional[int] = 0
   total_assists: Optional[int] = 0
   total_games: Optional[int] = 0
   skill_rating: Optional[float] = None
   positions: Optional[List[str]] = []

# Full Member
class MemberFull(BaseModel):
   id: int
   club_id: int
   user_id: int
   total_goals: int
   total_assists: int
   total_games: int
   skill_rating: Optional[float]
   positions: List[str]
   
   class Config:
       from_attributes = True