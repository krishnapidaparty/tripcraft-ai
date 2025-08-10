"""
MongoDB database configuration and models for TripCraft AI
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "tripcraft_ai"

# Database connection
client: Optional[AsyncIOMotorClient] = None
database = None

async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed!")

# Pydantic Models for MongoDB Documents
class UserSession(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    preferences: Dict[str, Any] = Field(default_factory=dict)

class TravelPlan(BaseModel):
    plan_id: str = Field(..., description="Unique plan identifier")
    session_id: str = Field(..., description="Associated session ID")
    destination: str = Field(..., description="Destination name")
    budget: str = Field(..., description="Budget range")
    style: str = Field(..., description="Travel style")
    duration: str = Field(..., description="Trip duration")
    itinerary: Dict[str, Any] = Field(default_factory=dict)
    reviews: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    message_id: str = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Associated session ID")
    user_message: str = Field(..., description="User's message")
    ai_response: str = Field(..., description="AI's response")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Destination(BaseModel):
    destination_id: str = Field(..., description="Unique destination identifier")
    name: str = Field(..., description="Destination name")
    country: str = Field(..., description="Country")
    description: str = Field(..., description="Destination description")
    travel_styles: List[str] = Field(default_factory=list)
    budget_range: str = Field(..., description="Budget range")
    best_time_to_visit: str = Field(..., description="Best time to visit")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Database Operations
class DatabaseManager:
    def __init__(self):
        self.db = database

    async def create_user_session(self, session_id: str, preferences: Dict[str, Any] = None) -> UserSession:
        """Create a new user session"""
        session = UserSession(
            session_id=session_id,
            preferences=preferences or {}
        )
        await self.db.sessions.insert_one(session.dict())
        return session

    async def get_user_session(self, session_id: str) -> Optional[UserSession]:
        """Get user session by ID"""
        session_data = await self.db.sessions.find_one({"session_id": session_id})
        if session_data:
            return UserSession(**session_data)
        return None

    async def update_user_session(self, session_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user session preferences"""
        result = await self.db.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "preferences": preferences,
                    "last_activity": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    async def save_travel_plan(self, travel_plan: TravelPlan) -> bool:
        """Save a travel plan"""
        result = await self.db.travel_plans.insert_one(travel_plan.dict())
        return result.inserted_id is not None

    async def get_travel_plans(self, session_id: str) -> List[TravelPlan]:
        """Get all travel plans for a session"""
        cursor = self.db.travel_plans.find({"session_id": session_id}).sort("created_at", -1)
        plans = []
        async for plan_data in cursor:
            plans.append(TravelPlan(**plan_data))
        return plans

    async def save_chat_message(self, chat_message: ChatMessage) -> bool:
        """Save a chat message"""
        result = await self.db.chat_messages.insert_one(chat_message.dict())
        return result.inserted_id is not None

    async def get_chat_history(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get chat history for a session"""
        cursor = self.db.chat_messages.find({"session_id": session_id}).sort("timestamp", -1).limit(limit)
        messages = []
        async for message_data in cursor:
            messages.append(ChatMessage(**message_data))
        return messages[::-1]  # Reverse to get chronological order

    async def save_destination(self, destination: Destination) -> bool:
        """Save a destination"""
        result = await self.db.destinations.insert_one(destination.dict())
        return result.inserted_id is not None

    async def search_destinations(self, query: str, limit: int = 10) -> List[Destination]:
        """Search destinations by name or description"""
        cursor = self.db.destinations.find({
            "$text": {"$search": query}
        }).limit(limit)
        destinations = []
        async for dest_data in cursor:
            destinations.append(Destination(**dest_data))
        return destinations

    async def get_popular_destinations(self, limit: int = 10) -> List[Destination]:
        """Get popular destinations"""
        cursor = self.db.destinations.find().sort("created_at", -1).limit(limit)
        destinations = []
        async for dest_data in cursor:
            destinations.append(Destination(**dest_data))
        return destinations

# Global database manager instance
db_manager = DatabaseManager()
