from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Event connection
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="games")
    # Teams playing (keys from event.teams)
    teams = Column(ARRAY(String), nullable=False)  # ["a", "c"]
    # Goals scored
    goals = Column(JSON, default=[])  # [{"team": "a", "scorer": 19, "assist": 22}]

    result = Column(JSON)  # {"team_a": 3, "team_b": 1}
    winner = Column(String) 
    
