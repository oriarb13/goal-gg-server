# schemas/event.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from app.models.enums import SportCategoryEnum, EventStatusEnum

# Create Event
class EventCreate(BaseModel):
   name: str
   description: str
   image: Optional[str] = "default-event.jpg"
   club_id: int
   field_id: Optional[int] = None
   location: dict  # {"address": "...", "lat": 32.0, "lng": 34.0}
   start_time: datetime
   end_time: datetime
   teams: Optional[Dict] = {}  # {"a": [19,22,31], "b": [40,50,26]}
   sport_category: SportCategoryEnum
   status: Optional[EventStatusEnum] = EventStatusEnum.UPCOMING
   max_participants: Optional[int] = 50
   min_participants_to_start: Optional[int] = 5
   cost: Optional[float] = 0.0

# Full Event
class EventFull(BaseModel):
   id: int
   name: str
   description: str
   image: str
   club_id: int
   field_id: Optional[int]
   location: dict
   start_time: datetime
   end_time: datetime
   teams: Dict
   sport_category: SportCategoryEnum
   status: EventStatusEnum
   max_participants: int
   min_participants_to_start: int
   cost: float
   created_at: datetime
   updated_at: Optional[datetime]
   
   class Config:
       from_attributes = True