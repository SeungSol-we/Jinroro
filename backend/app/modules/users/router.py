from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.auth.service import AuthService
from app.modules.users.schemas import AwardIn, CertificationIn, UserProfileOut, UserProfileUpdate, UserScoreUpdate
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["사용자"])
bearer = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    auth_service = AuthService(db)
    return await auth_service.get_current_user(creds.credentials)


@router.get("/me", response_model=UserProfileOut)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """내 프로필 조회"""
    service = UserService(db)
    return await service.get_my_profile(current_user.id)


@router.patch("/me")
async def update_my_profile(
    body: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """내 프로필 수정"""
    service = UserService(db)
    return await service.update_my_profile(current_user.id, body)


@router.post("/me/certifications", status_code=201)
async def add_certification(
    body: CertificationIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """자격증 추가"""
    service = UserService(db)
    return await service.add_certification(current_user.id, body)


@router.post("/me/awards", status_code=201)
async def add_award(
    body: AwardIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """수상 이력 추가"""
    service = UserService(db)
    return await service.add_award(current_user.id, body)


@router.put("/me/score")
async def update_score(
    body: UserScoreUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """성적 입력/수정"""
    service = UserService(db)
    return await service.update_score(current_user.id, body)
