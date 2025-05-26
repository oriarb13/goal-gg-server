from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict
import json

from app.core.database import get_db, SessionLocal
from app.core.logger import get_logger  
from app.utils.security import verify_token
from app.models.user import User

logger = get_logger(__name__)  

# active connections
active_connections: Dict[int, WebSocket] = {}

async def live_location(websocket: WebSocket, token: str):
    """handle WebSocket for user location"""
    
    # check token
    user_id_str = verify_token(token)
    if not user_id_str:
        await websocket.close(code=4001, reason="Invalid token")
        logger.error(f"❌ Invalid token: {token}")
        return
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        await websocket.close(code=4001, reason="Invalid user ID")
        logger.error(f"❌ Invalid user ID: {user_id_str}")
        return
    
    # get user
    await websocket.accept() #accept connection(async await)
    active_connections[user_id] = websocket
    
    logger.info(f" User {user_id} connected to location WebSocket")
    
    try:
        while True:
            # get location data
            data = await websocket.receive_text()
            new_location = json.loads(data)
            
            # check validity
            if "lat" not in new_location or "lng" not in new_location:
                await websocket.send_json({
                    "error": "Missing lat or lng"
                })
                logger.error(f"❌ Missing lat or lng: {new_location}")
                continue
            
            # update location in database
            db = SessionLocal()
            try:
                success = await update_location(
                    db, user_id, new_location
                )
                
                if success:
                    await websocket.send_json({
                        "status": "location updated",
                        "lat": new_location["lat"],
                        "lng": new_location["lng"]
                    })
                    logger.info(f"📍 Updated location for user {user_id}: {new_location['lat']}, {new_location['lng']}")
                else:
                    await websocket.send_json({
                        "error": "Failed to update location"
                    })
                    logger.error(f"❌ Failed to update location for user {user_id}")
                    
            finally:
                db.close()
                
    except WebSocketDisconnect:
        logger.info(f" User {user_id} disconnected from location WebSocket")
    except Exception as e:
        logger.error(f"❌ Error in location WebSocket for user {user_id}: {e}")
    finally:
        # clear connection
        if user_id in active_connections:
            del active_connections[user_id]

async def update_location(db: Session, user_id: int, new_location: dict) -> bool:
    """update user location in database"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.location = {
                "lat": float(new_location["lat"]),
                "lng": float(new_location["lng"])
            }
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Database error updating location: {e}")
        db.rollback()
        return False

def get_active_connections() -> Dict[int, WebSocket]:
    """return active connections"""
    return active_connections