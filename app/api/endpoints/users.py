from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.crud import user as crud_user
from app.models.user import User  
from app.schemas.user import UserCreate, UserLogin, UserFull
from app.utils.security import create_token
from app.utils.response import success_response, error_response
from app.api.deps import get_current_user
from app.core.logger import get_logger  

logger = get_logger(__name__)  
router = APIRouter()

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"POST /register - Registration attempt for: {user.email}")
    
    try:
        result = crud_user.register(db, user)
        logger.info(f"Registration successful for: {user.email}")
        return success_response(
            data=result,
            message="User registered successfully",
            status=201
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Registration processing error: {e}")
        return error_response(
            message=f"Registration failed: {str(e)}",
            status=500
        )

@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    logger.info(f"POST /login - Login attempt for: {user_data.email}")
    
    try:
        user = crud_user.login(db, user_data.email, user_data.password)
        token = create_token(str(user.id))
        
        login_data = {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }
        
        logger.info(f"Login successful for: {user_data.email} (ID: {user.id})")
        return success_response(
            data=login_data,
            message="Login successful",
            status=200
        )
        
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Login processing error: {e}")
        return error_response(
            message=f"Login processing failed: {str(e)}",
            status=500
        )

@router.get("/")
def get_all_users(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logger.info(f"GET /users - Fetching users (skip={skip}, limit={limit}) by user: {current_user.email}")
    
    try:
        result = crud_user.get_all_users(db, skip=skip, limit=limit)
        logger.info(f"Successfully returned users to: {current_user.email}")
        return success_response(
            data=result,
            message="Users retrieved successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Get users processing error: {e}")
        return error_response(
            message=f"Failed to retrieve users: {str(e)}",
            status=500
        )

@router.get("/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /users/{user_id} - Requested by: {current_user.email}")
    
    try:
        result = crud_user.get_user_by_id(db, user_id)
        logger.info(f"Successfully returned user {user_id} to: {current_user.email}")
        return success_response(
            data=result,
            message="User retrieved successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Get user processing error: {e}")
        return error_response(
            message=f"Failed to retrieve user: {str(e)}",
            status=500
        )

@router.put("/role")
def change_role(
    user_id: int,
    new_role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"PUT /role - Changing role for user {user_id} to {new_role_id} by: {current_user.email}")
    
    if user_id != current_user.id and current_user.role_id != 5:
        logger.warning(f"Unauthorized attempt to change role for user {user_id} by: {current_user.email}")
        return error_response(
            message="Unauthorized to change role",
            status=403
        )
    
    try:
        result = crud_user.change_role(db, user_id, new_role_id)
        logger.info(f"Successfully changed role for user {user_id} to {new_role_id} by: {current_user.email}")
        return success_response(
            data=result,
            message="Role changed successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Change role processing error: {e}")
        return error_response(
            message=f"Failed to change role: {str(e)}",
            status=500
        )
