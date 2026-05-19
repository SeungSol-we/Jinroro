from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    SignupRequest,
    TokenRefreshRequest,
    TokenResponse,
    UserOut,
)
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["인증"])
bearer = HTTPBearer()


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    """회원가입"""
    service = AuthService(db)
    return await service.signup(body.email, body.password)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """로그인"""
    service = AuthService(db)
    return await service.login(body.email, body.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """액세스 토큰 재발급"""
    service = AuthService(db)
    return await service.refresh(body.refresh_token)


@router.get("/me", response_model=UserOut)
async def me(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    """내 계정 정보"""
    service = AuthService(db)
    return await service.get_current_user(creds.credentials)
