from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship
class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  
    max_clubs = Column(Integer, default=0, nullable=False)
    max_players = Column(Integer, default=0, nullable=False)
    cost = Column(Float, default=0.0, nullable=False)
    users = relationship("User", back_populates="role")
    #timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())