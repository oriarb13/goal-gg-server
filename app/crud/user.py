from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user import UserCreate, UserFull
from app.utils.security import hash_password, verify_password
from app.core.logger import get_logger
from fastapi import HTTPException
from app.models.member import Member

logger = get_logger(__name__)

def register(db: Session, user: UserCreate) -> UserFull:
    logger.info(f"Attempting to register user: {user.email}")
    
    try:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            logger.warning(f"Email already exists: {user.email}")
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )
        
        # Convert Phone Pydantic model to dict
        phone_dict = user.phone.model_dump() if user.phone else {"prefix": None, "number": None}
        
        # Check for existing phone using JSON operations
        existing_phone = db.query(User).filter(
            User.phone['number'].astext == phone_dict.get('number')
        ).first()
        
        if existing_phone and phone_dict.get('number'):  # Only check if number is provided
            logger.warning(f"Phone number already exists: {phone_dict.get('number')}")
            raise HTTPException(
                status_code=409,
                detail="Phone number already registered"
            )
        
        hashed_password = hash_password(user.password)
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            phone=phone_dict,  # Use dict instead of Pydantic model
            sport_category=user.sport_category,
            year_of_birth=user.year_of_birth,
            city=user.city,
            country=user.country,
            role_id=1
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Successfully registered user: {user.email} with ID: {db_user.id}")
        return UserFull.model_validate(db_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to register user {user.email}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to register user: {str(e)}"
        )

def login(db: Session, email: str, password: str) -> UserFull:
    logger.info(f"Login attempt for email: {email}")
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"User not found: {email}")
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        if not verify_password(password, user.password):
            logger.warning(f"Invalid password for user: {email}")
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )
        
        logger.info(f"Successful login for user: {email} (ID: {user.id})")
        return UserFull.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {email}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserFull]:
    logger.info(f"Fetching users with skip={skip}, limit={limit}")
    
    try:
        # users = db.query(User).offset(skip).limit(limit).all()
        users = db.query(User)\
                .options(\
                    joinedload(User.role),
                    joinedload(User.memberships).joinedload(Member.club),
                    joinedload(User.owned_clubs)
                    
                )\
                .offset(skip)\
                .limit(limit)\
                .all()        
        logger.info(f"Successfully fetched {len(users)} users")
        return [UserFull.model_validate(user) for user in users]
        
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch users: {str(e)}"
        )

def get_user_by_id(db: Session, user_id: int) -> UserFull:
    logger.info(f"Fetching user by ID: {user_id}")
    
    try:
        # user = db.query(User).filter(User.id == user_id).first()
        user = db.query(User)\
                .options(\
                    joinedload(User.role),
                    joinedload(User.memberships).joinedload(Member.club),
                    joinedload(User.owned_clubs)
                    
                )\
                .filter(User.id == user_id)\
                .first()
        
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"User not found with ID: {user_id}"
            )
        
        logger.info(f"Found user: {user.email} (ID: {user_id})")
        return UserFull.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error fetching user: {str(e)}"
        )

def change_role(db: Session, user_id: int, new_role_id: int) -> UserFull:
    logger.info(f"Changing role for user {user_id} to {new_role_id}")
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"User not found with ID: {user_id}"
            )
        if new_role_id == 1 and len(user.owned_clubs) > 0:
            raise HTTPException(
                status_code=403,
                detail="Cannot change role to user if user has owned clubs"
            )
        if new_role_id == 2 and len(user.owned_clubs) > 1:
            raise HTTPException(
                status_code=403,
                detail="Cannot change role to silver if user has more than 1 club"
            )
        if new_role_id == 3 and len(user.owned_clubs) > 3:
            raise HTTPException(
                status_code=403,
                detail="Cannot change role to gold if user has more than 3 clubs"
            )
        if new_role_id == 4 and len(user.owned_clubs) > 5:
            raise HTTPException(
                status_code=403,
                detail="Cannot change role to premium if user has more than 5 clubs"
            )
        user.role_id = new_role_id
        db.commit()
        db.refresh(user)
        
        logger.info(f"Successfully changed role for user {user_id} to {new_role_id}")
        return UserFull.model_validate(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error changing role for user {user_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to change user role: {str(e)}"
        )

