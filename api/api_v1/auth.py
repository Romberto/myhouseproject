from fastapi import APIRouter, HTTPException
from starlette import status

from config import settings
from core.security.jwt import create_access_token, is_admin, verify_password
from servises.telegram_auth import verify_telegram_auth
from shemas.projects import AuthResponse, TelegramAuthData, PassLoginRequest

router=APIRouter(tags=["AUth"])

@router.post("/auth/telegram", response_model=AuthResponse)
async def telegram_login(auth_data: TelegramAuthData):
    auth_dict = auth_data.model_dump()
    if not verify_telegram_auth(auth_dict):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram authentication")
    user_id = auth_data.id
    token = create_access_token({"user_id": user_id})
    return AuthResponse(access_token=token, user_id=user_id, is_admin=is_admin(user_id))



@router.post("/login/password", response_model=AuthResponse)
async def login_with_password(data: PassLoginRequest):
    if data.login != settings.auth.login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # stored password НЕ хеширован → хешируем оба
    if not verify_password(data.password, settings.auth.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    user_id = settings.admin.id

    token = create_access_token({"user_id": user_id, "is_admin": True})

    return AuthResponse(
        access_token=token,
        user_id=user_id,
        is_admin=True
    )