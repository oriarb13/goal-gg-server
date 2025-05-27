from fastapi import FastAPI, WebSocket                    #the entry point of the application like express in node.js
from fastapi.middleware.cors import CORSMiddleware #cors

from app.core.config import settings #the config of the application


#routers
from app.api.endpoints import users, clubs


from app.websocket.location import live_location  #socket

#create the app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI application with PostgreSQL"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS, #allowed array
    allow_credentials=True, #cookies
    allow_methods=["*"], #all crud methods
    allow_headers=["*"], #all headers
)

# Include routers   //imported       //the rout      //swagger
app.include_router(users.router,   prefix="/users", tags=["users"])
app.include_router(clubs.router,   prefix="/clubs", tags=["clubs"])
@app.get("/")
async def root():
    return {"message": "Welcome to GoalGG API ori arbeli"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} #a must for docker

@app.websocket("/ws/location")
async def websocket_location(websocket: WebSocket, token: str):
    await live_location(websocket, token)