from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

#password hashing
pwd_context = CryptContext(schemes=["bcrypt"])

#hash the password
def hash_password(password: str) -> str:
   return pwd_context.hash(password)

#check if the password is correct
def verify_password(password: str, hashed_password: str) -> bool:
   return pwd_context.verify(password, hashed_password)

#create a JWT token with user ID
def create_token(user_id: str) -> str:  
   expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   data = {"sub": user_id, "exp": expire}  
   return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#check the JWT token and return the user ID
def verify_token(token: str) -> str | None:
   try:
       payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
       return payload.get("sub")  
   except JWTError:
       return None