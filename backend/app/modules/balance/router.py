from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.balance.schemas import AnswerRequest, AnswerOut, AvoidTagOut, ScenarioOut
from app.modules.balance.service import BalanceService
from app.modules.users.router import get_current_user

router = APIRouter(prefix="/balance", tags=["밸런스 게임"])


@router.get("/scenarios", response_model=list[ScenarioOut])
async def get_scenarios(db: AsyncSession = Depends(get_db)):
    """전체 시나리오 목록 (비로그인 가능)"""
    service = BalanceService(db)
    return await service.get_scenarios()


@router.get("/scenarios/{scenario_id}", response_model=ScenarioOut)
async def get_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    """시나리오 상세"""
    service = BalanceService(db)
    return await service.get_scenario(scenario_id)


@router.post("/answers", status_code=201)
async def submit_answer(
    body: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """밸런스 게임 답변 제출 → 싫음 보관함 자동 누적"""
    service = BalanceService(db)
    return await service.submit_answer(current_user.id, body)


@router.get("/history")
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """내 답변 히스토리"""
    service = BalanceService(db)
    return await service.get_history(current_user.id)


@router.get("/avoid-tags", response_model=list[AvoidTagOut])
async def get_avoid_tags(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """내 싫음 보관함 조회"""
    service = BalanceService(db)
    tags = await service.get_avoid_tags(current_user.id)
    return [{"tag_name": t.tag.tag_name, "accumulated_weight": t.accumulated_weight} for t in tags]
