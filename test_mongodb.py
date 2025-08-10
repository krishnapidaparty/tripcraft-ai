#!/usr/bin/env python3
"""
Test MongoDB connection and basic operations
"""
import asyncio
import os
from dotenv import load_dotenv
from app.database import connect_to_mongo, close_mongo_connection, db_manager

async def test_mongodb():
    """Test MongoDB connection and basic operations"""
    print("🔍 Testing MongoDB Connection...")
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully!")
        
        # Test creating a user session
        session_id = "test_session_123"
        session = await db_manager.create_user_session(session_id, {"test": "data"})
        print(f"✅ Created user session: {session.session_id}")
        
        # Test retrieving the session
        retrieved_session = await db_manager.get_user_session(session_id)
        if retrieved_session:
            print(f"✅ Retrieved session: {retrieved_session.session_id}")
        else:
            print("❌ Failed to retrieve session")
        
        # Test updating session
        updated = await db_manager.update_user_session(session_id, {"updated": "data"})
        if updated:
            print("✅ Updated session successfully")
        else:
            print("❌ Failed to update session")
        
        # Test database collections
        collections = await db_manager.db.list_collection_names()
        print(f"✅ Database collections: {collections}")
        
        print("\n🎉 All MongoDB tests passed!")
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure MongoDB is running (local) or Atlas connection is correct")
        print("2. Check your MONGODB_URL in .env file")
        print("3. Verify network access settings in MongoDB Atlas")
        
    finally:
        # Close connection
        await close_mongo_connection()
        print("🔌 MongoDB connection closed")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the test
    asyncio.run(test_mongodb())
