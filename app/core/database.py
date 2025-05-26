from sqlalchemy import create_engine, text  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

def create_database_engine():
    try:
        engine = create_engine(
            settings.DATABASE_URL, 
            echo=False,  
            pool_pre_ping=True,  #check the connection before use
            pool_size=10,  
            max_overflow=20  
        )
        logger.info("Successfully connected to the database")
        return engine
    
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}", exc_info=True)
        raise

#create the engine
engine = create_database_engine()

#create the session
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

#base for the models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
        