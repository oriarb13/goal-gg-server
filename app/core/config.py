from pydantic_settings import BaseSettings #take the settings from the .env file
from typing import List #for the allowed hosts

class Settings(BaseSettings): # Class Inheritance:
    PROJECT_NAME: str = "GoalGG API"
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "postgresql://postgres:ori13690@localhost:5432/goalgg" #db connection
    
    # jwt
    SECRET_KEY: str = "your-secret-key-here" 
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1000 
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"] 
    
    class Config:
        env_file = ".env"  #take the settings from the .env file

settings = Settings()