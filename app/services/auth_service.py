from fastapi import HTTPException, status
from app.models.user import UserCreate, UserResponse
from app.database import users_collection
from app.utils.security import hash_password, verify_password, create_access_token
from datetime import datetime
from bson import ObjectId

#auth_service.py is responsible for handling the business logic related to authentication, such as registering users, logging them in, and generating JWT tokens. It interacts with the database through the users_collection and uses utility functions for password hashing and token creation.

async def register_user(user_data: UserCreate) -> dict:
    # 1. Check if user already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password and prepare the database document
    hashed_password = hash_password(user_data.password)
    user_dict = {
        "name": user_data.name,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }

    # 3. Insert into MongoDB
    result = await users_collection.insert_one(user_dict)
    
    # 4. Return the response matching our UserResponse model
    return {
        "id": str(result.inserted_id),
        "name": user_dict["name"],
        "email": user_dict["email"],
        "created_at": user_dict["created_at"]
    }

async def login_user(email: str, password: str) -> str:
    # 1. Find the user
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2. Verify password
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. Create and return JWT token
    return create_access_token(data={"sub": str(user["_id"])})