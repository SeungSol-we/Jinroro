from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.fun.schemas import FaceReadingRequest, FortuneRequest, FunResultOut
from app.modules.fun.service import FunService
from app.modules.users.router import get_current_user

router = APIRouter(prefix="/fun", tags=["재미 기능"])


@router.post("/fortune", response_model=FunResultOut)
async def get_fortune(
    body: FortuneRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """오늘의 운세 (재미용, 추천 로직에 미반영)"""
    service = FunService(db)
    return await service.get_fortune(current_user.id, body.birth_date)


@router.post("/face-reading", response_model=FunResultOut)
async def get_face_reading(
    body: FaceReadingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """관상 분석 (재미용)"""
    service = FunService(db)
    return await service.get_face_reading(current_user.id, body.description)
