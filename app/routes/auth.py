from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate):
    return await register_user(user_data)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Swagger sends the email inside the 'username' field, so we pass that to our service
    token = await login_user(form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}