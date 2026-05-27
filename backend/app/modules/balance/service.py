from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequestException, NotFoundException
from app.modules.balance.repository import BalanceRepository
from app.modules.balance.schemas import AnswerRequest


class BalanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
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

    async def get_keyword_suggestions(self, user_id: int) -> list[dict]:
        """
        전체 fear_tag 목록을 반환하면서,
        각 태그가 이미 사용자의 싫음 보관함에 있는지 표시
        → 프론트에서 "이 중 싫은 거 골라봐" UI에 사용
        """
        all_tags = await self.repo.get_all_fear_tags()
        user_tags = await self.repo.get_user_fear_tags(user_id)
        user_tag_ids = {ut.tag_id for ut in user_tags}

        return [
            {
                "tag_id": tag.id,
                "tag_name": tag.tag_name,
                "description": tag.description,
                "already_in_box": tag.id in user_tag_ids,
            }
            for tag in all_tags
        ]

    async def add_tag_manually(self, user_id: int, tag_id: int) -> dict:
        """사용자가 직접 키워드를 싫음 보관함에 추가"""
        tag = await self.repo.get_fear_tag_by_id(tag_id)
        if not tag:
            from app.common.exceptions import NotFoundException
            raise NotFoundException("존재하지 않는 태그입니다.")
        await self.repo.upsert_fear_tag(user_id, tag_id, tag.tag_weight)
        return {"tag_id": tag_id, "tag_name": tag.tag_name, "message": "싫음 보관함에 추가되었습니다."}

    async def remove_tag_manually(self, user_id: int, tag_id: int) -> dict:
        """사용자가 직접 키워드를 싫음 보관함에서 제거"""
        deleted = await self.repo.delete_fear_tag(user_id, tag_id)
        if not deleted:
            from app.common.exceptions import NotFoundException
            raise NotFoundException("싫음 보관함에 해당 태그가 없습니다.")
        return {"tag_id": tag_id, "message": "싫음 보관함에서 제거되었습니다."}

    async def generate_ai_scenario(self, user_id: int) -> dict:
        """AI로 시나리오 생성 (테마 랜덤 + fear_tag 조합)"""
        from app.modules.balance.ai_generator import generate_scenario
        result = await generate_scenario(self.db, user_id)
        if not result:
            from app.common.exceptions import BadRequestException
            raise BadRequestException("시나리오를 생성할 수 없습니다. 배경 테마 또는 태그 데이터를 확인해주세요.")
        return result

    async def submit_ai_answer(self, user_id: int, body) -> dict:
        """
        AI 시나리오 답변 제출.
        선택한 선택지의 fear_tag를 싫음 보관함에 누적.
        """
        from app.common.exceptions import BadRequestException, NotFoundException

        if body.selected_label not in ("left", "right"):
            raise BadRequestException("selected_label은 'left' 또는 'right'여야 합니다.")

        ai_scenario = await self.repo.get_ai_scenario(body.ai_scenario_id)
        if not ai_scenario:
            raise NotFoundException("AI 시나리오를 찾을 수 없습니다.")

        # 선택한 레이블에 맞는 fear_tag_id 검증
        expected_tag_id = (
            ai_scenario.fear_tag_left_id
            if body.selected_label == "left"
            else ai_scenario.fear_tag_right_id
        )
        if body.selected_fear_tag_id != expected_tag_id:
            raise BadRequestException("선택한 태그 ID가 시나리오와 일치하지 않습니다.")

        # 싫음 보관함에 누적
        tag = await self.repo.get_fear_tag_by_id(body.selected_fear_tag_id)
        if tag:
            await self.repo.upsert_fear_tag(user_id, tag.id, tag.tag_weight)

        return {
            "message": "답변이 저장되었습니다.",
            "added_to_box": tag.tag_name if tag else None,
        }
