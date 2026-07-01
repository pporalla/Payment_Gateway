from fastapi import APIRouter
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate):
    return await register_user(user_data)

@router.post("/login")
async def login(email: str, password: str):
    token = await login_user(email, password)
    return {"access_token": token, "token_type": "bearer"}