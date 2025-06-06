from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.security import verify_token
from app.crud.user import get_user_by_id  
from app.models.user import User
from app.core.logger import get_logger  

logger = get_logger(__name__)  
security = HTTPBearer()

DEBUG_TOKEN = "ori13690"
DEBUG_USER_ID = 1

def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(security),
  db: Session = Depends(get_db)
) -> User:
  logger.info(" Attempting to authenticate user via token")
  
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
     # Debug mode bypass
  if credentials.credentials == DEBUG_TOKEN:
    logger.info(f" DEBUG MODE: Using debug token for user ID: {DEBUG_USER_ID}")
    user_data = get_user_by_id(db, DEBUG_USER_ID)
    if user_data is None:
        logger.error(f"❌ DEBUG: User not found in database for ID: {DEBUG_USER_ID}")
        raise credentials_exception
    logger.info(f"✅ DEBUG: User authenticated successfully: {user_data.email} (ID: {DEBUG_USER_ID})")
    return user_data
  # check token
  user_id_str = verify_token(credentials.credentials)  
  if user_id_str is None:
      logger.warning("❌ Invalid or expired token")
      raise credentials_exception
  
  # convert to int
  try:
      user_id = int(user_id_str)
      logger.info(f" Token validated for user ID: {user_id}")
  except ValueError:
      logger.error(f"❌ Invalid user ID format in token: {user_id_str}")
      raise credentials_exception
  
  # search user
  user_data = get_user_by_id(db, user_id)  
  if user_data is None:
      logger.warning(f"❌ User not found in database for ID: {user_id}")
      raise credentials_exception
  
  logger.info(f"✅ User authenticated successfully: {user_data.email} (ID: {user_id})")
  return user_data