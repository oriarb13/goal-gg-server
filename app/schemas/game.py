from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# Create Game
class GameCreate(BaseModel):
   name: str
   event_id: int
   teams: List[str]  # ["a", "c"]
   goals: Optional[List[Dict]] = []  # [{"team": "a", "scorer": 19, "assist": 22}]
   result: Optional[Dict] = None  # {"team_a": 3, "team_b": 1}
   winner: Optional[str] = None

# Full Game
class GameFull(BaseModel):
   id: int
   name: str
   event_id: int
   teams: List[str]
   goals: List[Dict]
   result: Optional[Dict]
   winner: Optional[str]
   
   class Config:
       from_attributes = True