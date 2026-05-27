from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.balance.schemas import (
    AnswerRequest, AnswerOut, AvoidTagOut, ScenarioOut,
    KeywordSuggestionOut, ManualTagRequest,
    AiAnswerRequest, AiScenarioOut,
)
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
    """밸런스 게임 답변 제출 → 선택한 선택지의 fear_tag가 싫음 보관함에 자동 누적"""
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
    """내 싫음 보관함 조회 (가중치 내림차순)"""
    service = BalanceService(db)
    tags = await service.get_avoid_tags(current_user.id)
    return [{"tag_name": t.tag.tag_name, "accumulated_weight": t.accumulated_weight} for t in tags]


@router.get("/keyword-suggestions", response_model=list[KeywordSuggestionOut])
async def get_keyword_suggestions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    게임 완료 후 '이 중 싫은 거 골라봐' UI에 사용.
    전체 성격 키워드 목록 + already_in_box 여부를 함께 반환.
    """
    service = BalanceService(db)
    return await service.get_keyword_suggestions(current_user.id)


@router.post("/avoid-tags/manual", status_code=201)
async def add_avoid_tag_manually(
    body: ManualTagRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사용자가 키워드를 직접 싫음 보관함에 추가"""
    service = BalanceService(db)
    return await service.add_tag_manually(current_user.id, body.tag_id)


@router.delete("/avoid-tags/{tag_id}")
async def remove_avoid_tag_manually(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사용자가 키워드를 싫음 보관함에서 직접 제거"""
    service = BalanceService(db)
    return await service.remove_tag_manually(current_user.id, tag_id)


# ── AI 생성 시나리오 ───────────────────────────────────────────

@router.get("/ai/scenario", response_model=AiScenarioOut)
async def get_ai_scenario(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    AI가 생성하는 병맛 밸런스 게임 시나리오 1개 반환.
    배경 테마 랜덤 선택 + 아직 탐색 안 한 fear_tag 조합으로 생성.
    """
    service = BalanceService(db)
    return await service.generate_ai_scenario(current_user.id)


@router.post("/ai/answers", status_code=201)
async def submit_ai_answer(
    body: AiAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    AI 시나리오 답변 제출 → 선택한 쪽의 fear_tag가 싫음 보관함에 누적.
    body: { ai_scenario_id, selected_label: "left"|"right", selected_fear_tag_id }
    """
    service = BalanceService(db)
    return await service.submit_ai_answer(current_user.id, body)
