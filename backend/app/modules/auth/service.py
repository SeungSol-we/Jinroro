from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import ConflictException, UnauthorizedException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)

    async def signup(self, email: str, password: str) -> TokenResponse:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ConflictException("이미 사용 중인 이메일입니다.")

        hashed = hash_password(password)
        user = await self.repo.create(email=email, hashed_password=hashed)

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.")
        if not user.is_active:
            raise UnauthorizedException("비활성화된 계정입니다.")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("유효하지 않은 리프레시 토큰입니다.")

        user_id = int(payload["sub"])
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("사용자를 찾을 수 없습니다.")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def get_current_user(self, token: str):
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise UnauthorizedException("유효하지 않은 토큰입니다.")

        user = await self.repo.get_by_id(int(payload["sub"]))
        if not user:
            raise UnauthorizedException("사용자를 찾을 수 없습니다.")
        return user
