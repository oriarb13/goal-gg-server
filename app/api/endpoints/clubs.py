from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.crud import club as crud_club
from app.models.user import User
from app.schemas.club import ClubCreate, ClubFull
from app.models.enums import SportCategoryEnum
from app.utils.response import success_response, error_response
from app.api.deps import get_current_user
from app.core.logger import get_logger

# pubsub
from fastapi.responses import StreamingResponse
from app.core.sse_manager import sse_manager
import asyncio

logger = get_logger(__name__)
router = APIRouter()

@router.post("/")
def create_club(
    club: ClubCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"POST /clubs - Creating club: {club.name} by user: {current_user.email}")
    
    try:
        result = crud_club.create_club(db, club, current_user)
        logger.info(f"Club creation successful for: {current_user.email}")
        return success_response(
            data=result,
            message="Club created successfully",
            status=201
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Club creation processing error: {e}")
        return error_response(
            message=f"Failed to create club: {str(e)}",
            status=500
        )

@router.get("/search")
def search_clubs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Search by club name"),
    sort_by: str = Query("name", description="Sort by: name, created_at, members_count, distance"),
    sport_category: Optional[SportCategoryEnum] = Query(None, description="Filter by sport category"),
    is_private: Optional[bool] = Query(None, description="Filter by privacy status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    logger.info(f"GET /clubs/search - Search request by user: {current_user.email}")
    
    try:
        result = crud_club.search_clubs(
            current_user=current_user,
            db=db,
            name=name,
            sort_by=sort_by,
            sport_category=sport_category,
            is_private=is_private,
            skip=skip,
            limit=limit
        )
        logger.info(f"Search completed for user: {current_user.email}")
        return success_response(
            data=result,
            message="Clubs retrieved successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Search clubs processing error: {e}")
        return error_response(
            message=f"Failed to search clubs: {str(e)}",
            status=500
        )

@router.get("/my-clubs")
def get_my_clubs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /clubs/my-clubs - Request by user: {current_user.email}")
    
    try:
        result = crud_club.get_user_clubs(db, current_user)
        logger.info(f"User clubs retrieved for: {current_user.email}")
        return success_response(
            data=result,
            message="User clubs retrieved successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Get user clubs processing error: {e}")
        return error_response(
            message=f"Failed to retrieve user clubs: {str(e)}",
            status=500
        )

@router.get("/{club_id}")
def get_club(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /clubs/{club_id} - Requested by: {current_user.email}")
    
    try:
        result = crud_club.get_club_by_id(db, club_id)
        logger.info(f"Club {club_id} retrieved for: {current_user.email}")
        return success_response(
            data=result,
            message="Club retrieved successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Get club processing error: {e}")
        return error_response(
            message=f"Failed to retrieve club: {str(e)}",
            status=500
        )

@router.post("/{club_id}/join")
def join_club(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"POST /clubs/{club_id}/join - Request by user: {current_user.email}")
    
    try:
        result = crud_club.join_club(db, club_id, current_user)
        logger.info(f"Join club {club_id} processed for: {current_user.email}")
        
        message = "Join request sent successfully" if result.get("request_status") == "pending" else \
                 "Join request already pending" if result.get("request_status") == "already_pending" else \
                 "Successfully joined the club"
        
        status_code = 200 if "request_status" in result else 201
        
        return success_response(
            data=result,
            message=message,
            status=status_code
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Join club processing error: {e}")
        return error_response(
            message=f"Failed to join club: {str(e)}",
            status=500
        )

@router.post("/{club_id}/accept-request/{request_id}")
def accept_request(
    club_id: int,
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"POST /clubs/{club_id}/accept-request/{request_id} - Request by user: {current_user.email}")
    
    try:
        result = crud_club.accept_request(db, club_id, current_user, request_id)
        logger.info(f"Accept request {request_id} for club {club_id} processed by: {current_user.email}")
        return success_response(
            data=result,
            message="Request accepted successfully",
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Accept request processing error: {e}")
        return error_response(
            message=f"Failed to accept request: {str(e)}",
            status=500
        )

@router.delete("/{club_id}/leave")
def leave_club(
    club_id: int,
    user_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"DELETE /clubs/{club_id}/leave - Request by user: {current_user.email}")
    
    try:
        result = crud_club.leave_club(db, club_id, current_user, user_id)
        
        message = f"User removed from club successfully" if user_id else "Successfully left the club"
        
        logger.info(f"Leave club {club_id} processed for: {current_user.email}")
        return success_response(
            data=result,
            message=message,
            status=200
        )
    except HTTPException as e:
        return error_response(
            message=e.detail,
            status=e.status_code
        )
    except Exception as e:
        logger.error(f"Leave club processing error: {e}")
        return error_response(
            message=f"Failed to leave club: {str(e)}",
            status=500
        )


# pubsub
@router.get("/notifications/stream")
async def club_notifications_stream(
    current_user: User = Depends(get_current_user)
):
    """
    SSE endpoint for real-time club notifications
    מיועד לאדמינים שרוצים לקבל התראות על פעילות במועדונים שלהם
    """
    logger.info(f"SSE connection initiated by user: {current_user.email}")
    
    async def event_generator():
        # יצירת חיבור SSE עבור המשתמש
        queue = await sse_manager.connect(current_user.id)
        
        try:
            # שלח heartbeat ראשוני
            yield f"data: {{'type': 'connected', 'message': 'החיבור הוקם בהצלחה'}}\n\n"
            
            while True:
                try:
                    # המתן לאירוע חדש (עם timeout של 30 שניות)
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield event.to_sse_format()
                    
                except asyncio.TimeoutError:
                    # שלח heartbeat כדי לשמור על החיבור חי
                    yield f"data: {{'type': 'heartbeat', 'timestamp': '{asyncio.get_event_loop().time()}'}}\n\n"
                    
                except Exception as e:
                    logger.error(f"Error in SSE event generator for user {current_user.id}: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"SSE connection error for user {current_user.id}: {e}")
        finally:
            # ניקוי החיבור
            await sse_manager.disconnect(current_user.id, queue)
            logger.info(f"SSE connection closed for user: {current_user.email}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )