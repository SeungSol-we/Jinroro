from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.recommend.schemas import RecommendResultOut
from app.modules.recommend.service import RecommendService
from app.modules.users.router import get_current_user

router = APIRouter(prefix="/recommend", tags=["추천"])


@router.get("/result", response_model=RecommendResultOut)
async def get_recommend_result(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    싫음 보관함 + 포트폴리오 기반 직무 추천 결과 반환.
    점수 높은 순서로 정렬됨.
    """
    service = RecommendService(db)
    return await service.get_result(current_user.id)
