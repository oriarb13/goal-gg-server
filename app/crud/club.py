from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case, and_, or_
from typing import Optional, List
from app.models.club import Club
from app.schemas.club import ClubCreate, ClubFull
from app.models.enums import SportCategoryEnum
from app.core.logger import get_logger
from app.models.user import User
from app.models.member import Member
from app.models.enums import ClubStatusEnum
from fastapi import HTTPException
from app.core.sse_manager import sse_manager, create_club_join_event, create_member_joined_event, create_member_approved_event

logger = get_logger(__name__)

def create_club(db: Session, club: ClubCreate, current_user: User) -> ClubFull:
    logger.info(f"Creating club: {club.name} by admin: {current_user.id}")
    
    try:
        current_clubs_count = len(current_user.owned_clubs)
        if current_clubs_count >= current_user.role.max_clubs:
            logger.warning(f"User {current_user.id} reached max clubs limit: {current_user.role.max_clubs}")
            raise HTTPException(
                status_code=403,
                detail=f"Maximum {current_user.role.max_clubs} clubs allowed for your role"
            )
        
        # Convert Location Pydantic model to dict
        location_dict = club.location.model_dump() if club.location else {
            "country": None,
            "city": None, 
            "address": None,
            "lat": None,
            "lng": None
        }
        
        db_club = Club(
            name=club.name,
            description=club.description,
            image=club.image,
            admin_id=current_user.id,
            sport_category=club.sport_category,
            is_private=club.is_private,
            max_players=current_user.role.max_players,
            status=ClubStatusEnum.ACTIVE,
            location=location_dict,  # Use dict instead of Pydantic model
            captains_ids=[],
            pending_requests=[]
        )
        
        db.add(db_club)
        db.flush()
        
        db_member = Member(
            user_id=current_user.id,
            club_id=db_club.id,  
            total_goals=0,
            total_assists=0,
            total_games=0,
            skill_rating=current_user.avg_skill_rating,  
            positions=current_user.positions  
        )
        
        db.add(db_member)
        db.flush()
        db.commit()
        db.refresh(db_club)
        
        logger.info(f"Club created successfully: {club.name} (ID: {db_club.id})")
        return ClubFull.model_validate(db_club)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create club {club.name}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create club: {str(e)}"
        )

# Helper function to convert Club model to dict with captains
def populate_captains(club: Club) -> dict:
    """
    Convert Club model to dict with captains
    """
    # Get all fields from the model
    club_dict = {}
    for column in club.__table__.columns:
        club_dict[column.name] = getattr(club, column.name) # Get the value of the column
    
    # Add already loaded relationships
    club_dict['admin'] = club.admin
    club_dict['members'] = club.members
    
    # Find captains from the members based on captains_ids
    captains = []
    if club.captains_ids and club.members:
        captains = [member for member in club.members if member.id in club.captains_ids]
        logger.info(f"Found {len(captains)} captains for club {club.id}")
    
    club_dict['captains'] = captains
    
    return club_dict

def search_clubs(
    current_user: User,
    db: Session, 
    name: Optional[str] = None,
    sort_by: str = "name",
    sport_category: Optional[SportCategoryEnum] = None,
    is_private: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[ClubFull]:
    logger.info(f"Searching clubs - name: {name}, sort: {sort_by}, sport: {sport_category}, private: {is_private}, skip: {skip}, limit: {limit}")
    
    try:
        query = db.query(Club)\
                .options(
                    joinedload(Club.members).joinedload(Member.user),
                    joinedload(Club.admin)
                )
        
        if name:
            query = query.filter(Club.name.ilike(f"%{name}%"))
        
        if sport_category:
            query = query.filter(Club.sport_category == sport_category)
        
        if is_private is not None:
            query = query.filter(Club.is_private == is_private)
        
        if sort_by == "name":
            query = query.order_by(Club.name)
        elif sort_by == "created_at":
            query = query.order_by(Club.created_at.desc())
        elif sort_by == "members_count":
            query = query.outerjoin(Club.members).group_by(Club.id).order_by(func.count(Club.members).desc())
        elif sort_by == "distance":
            if not current_user.location or not current_user.location.get('lat') or not current_user.location.get('lng'):
                raise HTTPException(
                    status_code=400,
                    detail="User location is required for distance sorting"
                )
            
            user_lat = current_user.location['lat']
            user_lng = current_user.location['lng']
            
            distance_calc = func.sqrt(
                func.power(func.cast(Club.location['lat'].astext, func.Float()) - user_lat, 2) +
                func.power(func.cast(Club.location['lng'].astext, func.Float()) - user_lng, 2)
            )
            query = query.order_by(distance_calc)
        else:
            query = query.order_by(Club.name)

        clubs = query.offset(skip).limit(limit).all()
        logger.info(f"Found {len(clubs)} clubs matching criteria")
        
        # Work on each club separately to add captains
        result = []
        for club in clubs:
            club_dict = populate_captains(club)
            result.append(ClubFull.model_validate(club_dict))
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to search clubs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search clubs: {str(e)}"
        )

def get_club_by_id(db: Session, club_id: int) -> ClubFull:
    logger.info(f"Fetching club by ID: {club_id}")
    
    try:
        club = db.query(Club)\
                .options(
                    joinedload(Club.members).joinedload(Member.user),
                    joinedload(Club.admin)
                )\
                .filter(Club.id == club_id)\
                .first()
        if not club:
            logger.warning(f"Club not found with ID: {club_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Club not found with ID: {club_id}"
            )
        
        logger.info(f"Found club: {club.name} (ID: {club_id})")
        club_dict = populate_captains(club)
        return ClubFull.model_validate(club_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error fetching club {club_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error fetching club: {str(e)}"
        )

def get_user_clubs(db: Session, current_user: User) -> dict:
    logger.info(f"Fetching clubs for user: {current_user.id}")
    
    try:
        # Load owned clubs with relationships
        owned_clubs_query = db.query(Club)\
                          .options(
                              joinedload(Club.members).joinedload(Member.user),
                              joinedload(Club.admin)
                          )\
                          .filter(Club.admin_id == current_user.id)\
                          .all()
        
        owned_clubs = []
        for club in owned_clubs_query:
            club_dict = populate_captains(club)
            owned_clubs.append(ClubFull.model_validate(club_dict))
        
        # Load member clubs with relationships
        member_clubs_query = db.query(Club)\
                           .options(
                               joinedload(Club.members).joinedload(Member.user),
                               joinedload(Club.admin)
                           )\
                           .join(Member, Club.id == Member.club_id)\
                           .filter(Member.user_id == current_user.id)\
                           .filter(Club.admin_id != current_user.id)\
                           .all()
        
        member_clubs = []
        for club in member_clubs_query:
            club_dict = populate_captains(club)
            member_clubs.append(ClubFull.model_validate(club_dict))
        
        result_data = {
            "owned_clubs": owned_clubs,
            "member_clubs": member_clubs,
            "total_clubs": len(owned_clubs) + len(member_clubs)
        }
        
        logger.info(f"User {current_user.id} has {result_data['total_clubs']} clubs ({len(owned_clubs)} owned, {len(member_clubs)} member)")
        return result_data
        
    except Exception as e:
        logger.error(f"Failed to get user clubs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get user clubs: {str(e)}"
        )

def join_club(db: Session, club_id: int, current_user: User) -> dict:
    logger.info(f"User {current_user.id} attempting to join club {club_id}")
    
    try:
        club = db.query(Club)\
                .options(
                    joinedload(Club.members).joinedload(Member.user),
                    joinedload(Club.admin)
                )\
                .filter(Club.id == club_id)\
                .first()
        
        # check if club exists
        if not club:
            raise HTTPException(
                status_code=404,
                detail=f"Club not found with ID: {club_id}"
            )
        
        # check if user is already a member
        existing_member = db.query(Member).filter(
            Member.club_id == club_id,
            Member.user_id == current_user.id
        ).first()
        
        if existing_member:
            raise HTTPException(
                status_code=409,
                detail="User is already a member of this club"
            )
        
        # check if club is full
        current_members_count = len(club.members)
        if current_members_count >= club.max_players:
            raise HTTPException(
                status_code=403,
                detail="Club has reached maximum members limit"
            )
        
        # check if club is private
        if club.is_private:
            current_requests = list(club.pending_requests or [])
        
            if current_user.id not in current_requests:
                current_requests.append(current_user.id)
                club.pending_requests = current_requests
            
                db.commit()
                
                # 🆕 שלח SSE event לאדמין על בקשה חדשה
                user_name = f"{current_user.first_name} {current_user.last_name}"
                event = create_club_join_event(
                    club_id=club_id,
                    user_id=current_user.id,
                    user_name=user_name,
                    admin_id=club.admin_id
                )
                
                # שלח באופן אסינכרוני (לא חוסם)
                import asyncio
                try:
                    asyncio.create_task(sse_manager.send_to_user(club.admin_id, event))
                except RuntimeError:
                    # אם אין event loop פעיל, נדלג על השליחה
                    logger.warning(f"Could not send SSE event - no active event loop")
                
                logger.info(f"Added user {current_user.id} to pending requests for club {club_id} and sent SSE notification")
                return {"request_status": "pending"}
            else:
                return {"request_status": "already_pending"}
        
        # add user to club (public club)
        new_member = Member(
            user_id=current_user.id,
            club_id=club_id,
            total_goals=0,
            total_assists=0,
            total_games=0,
            skill_rating=current_user.avg_skill_rating,
            positions=current_user.positions
        )
        
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        
        # 🆕 שלח SSE event על הצטרפות מוצלחת למועדון ציבורי
        user_name = f"{current_user.first_name} {current_user.last_name}"
        event = create_member_joined_event(
            club_id=club_id,
            user_id=current_user.id,
            user_name=user_name
        )
        
        # שלח לאדמין
        import asyncio
        try:
            asyncio.create_task(sse_manager.send_to_user(club.admin_id, event))
        except RuntimeError:
            logger.warning(f"Could not send SSE event - no active event loop")
        
        logger.info(f"User {current_user.id} joined club {club_id} successfully")
        return {"membership_status": "joined"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to join club {club_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to join club: {str(e)}"
        )

def accept_request(db: Session, club_id: int, current_user: User, request_id: int) -> dict:
    logger.info(f"User {current_user.id} attempting to accept request for club {club_id}")
    try:
        club = db.query(Club).filter(Club.id == club_id).first()
        user_request = db.query(User).filter(User.id == request_id).first()
        
        if not club:
            logger.warning(f"Club not found with ID: {club_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Club not found with ID: {club_id}"
            )
        
        if club.admin_id != current_user.id and current_user.role.id != 5:
            logger.warning(f"User {current_user.id} is not the admin of club {club_id}")
            raise HTTPException(
                status_code=403,
                detail="Only club admin can accept requests"
            )

        if request_id not in club.pending_requests:
            logger.warning(f"Request not found with ID: {request_id} in club {club_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Request not found with ID: {request_id}"
            )

        # add user to club
        new_member = Member(
            user_id=request_id,
            club_id=club_id,
            total_goals=0,
            total_assists=0,
            total_games=0,
            skill_rating=user_request.avg_skill_rating,
            positions=user_request.positions
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        # remove request from pending_requests
        current_requests = list(club.pending_requests or [])
        if request_id in current_requests:
            current_requests.remove(request_id)
            club.pending_requests = current_requests
        db.commit()

        # 🆕 שלח SSE events
        user_name = f"{user_request.first_name} {user_request.last_name}"
        
        # 1. שלח לאדמין שהבקשה אושרה
        admin_event = create_member_joined_event(
            club_id=club_id,
            user_id=request_id,
            user_name=user_name
        )
        
        # 2. שלח למשתמש שהבקשה שלו אושרה
        user_event = create_member_approved_event(
            club_id=club_id,
            user_id=request_id,
            user_name=user_name
        )
        
        import asyncio
        try:
            # שלח לשני המשתמשים
            asyncio.create_task(sse_manager.send_to_user(current_user.id, admin_event))
            asyncio.create_task(sse_manager.send_to_user(request_id, user_event))
        except RuntimeError:
            logger.warning(f"Could not send SSE events - no active event loop")

        logger.info(f"Request accepted for club {club_id} by user {current_user.id}")
        return {
            "membership_status": "joined",
            "user_id": request_id,
            "user_name": user_name
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to accept request for club {club_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to accept request: {str(e)}"
        )
    


def leave_club(db: Session, club_id: int, current_user: User , user_id: Optional[int] = None) -> dict:
    logger.info(f"User {current_user.id} attempting to leave club {club_id}")
    
    try:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise HTTPException(
                status_code=404,
                detail=f"Club not found with ID: {club_id}"
            )
        
        if club.admin_id == current_user.id and user_id == None or user_id == club.admin_id:
            raise HTTPException(
                status_code=403,
                detail="Club admin cannot leave the club"
            )
        if current_user.role.id != 5 and current_user.role.id != club.admin_id and user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Only club admin or super admin can remove a member from the club"
            )
        if user_id:
            member = db.query(Member).filter(
                Member.club_id == club_id,
                Member.user_id == user_id
            ).first()
        else:
            member = db.query(Member).filter(
                Member.club_id == club_id,
                Member.user_id == current_user.id
            ).first()
        
        if not member:
            raise HTTPException(
                status_code=404,
                detail="User is not a member of this club"
            )
        
        # Remove from captains_ids if member is captain
        if club.captains_ids and member.id in club.captains_ids:
            current_captains = list(club.captains_ids)
            current_captains.remove(member.id)
            club.captains_ids = current_captains
        
        db.delete(member)
        db.commit()
        
        logger.info(f"User {current_user.id} left club {club_id} successfully")
        return {"membership_status": "left"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to leave club {club_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to leave club: {str(e)}"
        )