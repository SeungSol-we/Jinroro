from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequestException, NotFoundException
from app.modules.balance.repository import BalanceRepository
from app.modules.balance.schemas import AnswerRequest


class BalanceService:
    def __init__(self, db: AsyncSession):
        self.repo = BalanceRepository(db)

    async def get_scenarios(self):
        return await self.repo.get_all_scenarios()

    async def get_scenario(self, scenario_id: int):
        scenario = await self.repo.get_scenario(scenario_id)
        if not scenario:
            raise NotFoundException("시나리오를 찾을 수 없습니다.")
        return scenario

    async def submit_answer(self, user_id: int, body: AnswerRequest):
        # 시나리오 유효성 확인
        scenario = await self.repo.get_scenario(body.scenario_id)
        if not scenario:
            raise NotFoundException("시나리오를 찾을 수 없습니다.")

        # 선택지가 해당 시나리오에 속하는지 확인
        choice = await self.repo.get_choice(body.selected_choice_id)
        if not choice or choice.scenario_id != body.scenario_id:
            raise BadRequestException("해당 시나리오의 선택지가 아닙니다.")

        # 답변 저장
        answer = await self.repo.save_answer(user_id, body.scenario_id, body.selected_choice_id)

        # 선택한 선택지에 fear_tag가 있으면 싫음 보관함에 누적
        if choice.fear_tag:
            await self.repo.upsert_fear_tag(user_id, choice.fear_tag_id, choice.fear_tag.tag_weight)

        return answer

    async def get_history(self, user_id: int):
        return await self.repo.get_user_answers(user_id)

    async def get_avoid_tags(self, user_id: int):
        """사용자의 싫음 보관함 반환 (가중치 내림차순)"""
        return await self.repo.get_user_fear_tags(user_id)
