from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.balance.schemas import (
    AnswerRequest, AvoidTagOut, TrashTagOut, ScenarioOut,
    KeywordSuggestionOut, ManualTagRequest,
    AiAnswerRequest, AiScenarioOut, JobAnalysisOut,
)
from app.modules.balance.service import BalanceService
from app.modules.users.router import get_current_user

router = APIRouter(prefix="/balance", tags=["밸런스 게임"])


@router.get("/scenarios", response_model=list[ScenarioOut])
async def get_scenarios(db: AsyncSession = Depends(get_db)):
    service = BalanceService(db)
    return await service.get_scenarios()


@router.get("/scenarios/{scenario_id}", response_model=ScenarioOut)
async def get_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    service = BalanceService(db)
    return await service.get_scenario(scenario_id)


@router.post("/answers", status_code=201)
async def submit_answer(
    body: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.submit_answer(current_user.id, body)


@router.get("/history")
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.get_history(current_user.id)


@router.get("/avoid-tags", response_model=list[AvoidTagOut])
async def get_avoid_tags(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    tags = await service.get_avoid_tags(current_user.id, include_deleted=False)
    return [
        {
            "id": t.id, 
            "tag_id": t.tag_id, 
            "tag_name": t.tag.tag_name, 
            "accumulated_weight": t.accumulated_weight,
            "description": t.tag.description
        } for t in tags
    ]


# 💡 [교정] response_model을 TrashTagOut으로 변경 및 안전한 None 매핑 추가
@router.get("/trash-tags", response_model=list[TrashTagOut])
async def get_trash_tags(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    tags = await service.get_avoid_tags(current_user.id, include_deleted=True)
    return [
        {
            "id": t.id, 
            "tag_id": t.tag_id, 
            "tag_name": t.tag.tag_name, 
            "accumulated_weight": t.accumulated_weight,
            "description": t.tag.description
        } for t in tags
    ]


@router.get("/keyword-suggestions", response_model=list[KeywordSuggestionOut])
async def get_keyword_suggestions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.get_keyword_suggestions(current_user.id)


@router.post("/avoid-tags/manual", status_code=201)
async def add_avoid_tag_manually(
    body: ManualTagRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.add_tag_manually(current_user.id, body.tag_id)


@router.delete("/avoid-tags/{tag_id}")
async def remove_avoid_tag_manually(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.soft_remove_tag(current_user.id, tag_id)


@router.post("/avoid-tags/{tag_id}/restore")
async def restore_avoid_tag_manually(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.restore_tag(current_user.id, tag_id)


# 💡 [교정] response_model을 JobAnalysisOut 리포트 객체 형식으로 올바르게 수정
@router.post("/analysis", response_model=JobAnalysisOut)
async def analyze_unfit_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.analyze_unfit_jobs(current_user.id)


# ── AI 생성 시나리오 ──

@router.get("/ai/scenario", response_model=AiScenarioOut)
async def get_ai_scenario(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = BalanceService(db)
    return await service.generate_ai_scenario(current_user.id)


@router.post("/ai/answers", status_code=201)
async def submit_ai_answer(
    body: AiAnswerRequest,  # 👈 이렇게 명시적으로 타입을 적어주세요!
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    AI 시나리오 답변 제출 → 선택한 쪽의 fear_tag가 싫음 보관함에 누적.
    """
    service = BalanceService(db)
    return await service.submit_ai_answer(current_user.id, body)