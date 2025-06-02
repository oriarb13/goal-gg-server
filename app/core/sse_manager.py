import asyncio
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SSEEvent:
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_sse_format(self) -> str:
        """Convert event to SSE format"""
        return f"data: {json.dumps({'type': self.event_type, 'data': self.data, 'timestamp': self.timestamp.isoformat()})}\n\n"

class SSEManager:
    def __init__(self):
        # Dictionary to store active connections
        # Format: {user_id: [queue1, queue2, ...]}
        self._connections: Dict[int, List[asyncio.Queue]] = {}
    
    async def connect(self, user_id: int) -> asyncio.Queue:
        """Add a new connection for a user"""
        queue = asyncio.Queue()
        
        if user_id not in self._connections:
            self._connections[user_id] = []
        
        self._connections[user_id].append(queue)
        print(f"User {user_id} connected to SSE. Active connections: {len(self._connections[user_id])}")
        return queue
    
    async def disconnect(self, user_id: int, queue: asyncio.Queue):
        """Remove a connection for a user"""
        if user_id in self._connections and queue in self._connections[user_id]:
            self._connections[user_id].remove(queue)
            
            # Clean up empty connection list
            if not self._connections[user_id]:
                del self._connections[user_id]
                
            print(f"User {user_id} disconnected from SSE")
    
    async def send_to_user(self, user_id: int, event: SSEEvent):
        """Send event to a specific user"""
        if user_id not in self._connections:
            print(f"No active connections for user {user_id}")
            return
        
        # Send to all connections for this user (multiple tabs/devices)
        for queue in self._connections[user_id][:]:  # Create copy to avoid modification during iteration
            try:
                await queue.put(event)
                print(f"Event sent to user {user_id}: {event.event_type}")
            except Exception as e:
                print(f"Failed to send event to user {user_id}: {e}")
                # Remove broken connection
                self._connections[user_id].remove(queue)
    
    async def send_to_multiple_users(self, user_ids: List[int], event: SSEEvent):
        """Send event to multiple users"""
        for user_id in user_ids:
            await self.send_to_user(user_id, event)
    
    async def broadcast_club_event(self, club_id: int, admin_id: int, event: SSEEvent):
        """Send event to club admin"""
        await self.send_to_user(admin_id, event)
    
    def get_active_connections_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(queues) for queues in self._connections.values())
    
    def get_connected_users(self) -> List[int]:
        """Get list of currently connected user IDs"""
        return list(self._connections.keys())

# Global SSE manager instance
sse_manager = SSEManager()

# Event helper functions
def create_club_join_event(club_id: int, user_id: int, user_name: str, admin_id: int) -> SSEEvent:
    """Create a club join event"""
    return SSEEvent(
        event_type="club:join-request",
        data={
            "club_id": club_id,
            "user_id": user_id,
            "user_name": user_name,
            "admin_id": admin_id,
            "message": f"{user_name} רוצה להצטרף למועדון"
        }
    )

def create_member_joined_event(club_id: int, user_id: int, user_name: str) -> SSEEvent:
    """Create a member joined event"""
    return SSEEvent(
        event_type="club:user-joined",
        data={
            "club_id": club_id,
            "user_id": user_id,
            "user_name": user_name,
            "message": f"{user_name} הצטרף למועדון בהצלחה"
        }
    )

def create_member_approved_event(club_id: int, user_id: int, user_name: str) -> SSEEvent:
    """Create a member approved event"""
    return SSEEvent(
        event_type="club:request-approved",
        data={
            "club_id": club_id,
            "user_id": user_id,
            "user_name": user_name,
            "message": f"הבקשה שלך למועדון אושרה!"
        }
    )