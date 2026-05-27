# app/modules/balance/service.py
import httpx
import os
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.exceptions import BadRequestException, NotFoundException
from app.modules.balance.repository import BalanceRepository
from app.modules.balance.schemas import AnswerRequest

class BalanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = BalanceRepository(db)

    async def get_scenarios(self): return await self.repo.get_all_scenarios()
    async def get_scenario(self, scenario_id: int):
        scenario = await self.repo.get_scenario(scenario_id)
        if not scenario: raise NotFoundException("시나리오 없음")
        return scenario

    async def submit_answer(self, user_id: int, body: AnswerRequest):
        scenario = await self.repo.get_scenario(body.scenario_id)
        choice = await self.repo.get_choice(body.selected_choice_id)
        answer = await self.repo.save_answer(user_id, body.scenario_id, body.selected_choice_id)
        if choice.fear_tag:
            await self.repo.upsert_fear_tag(user_id, choice.fear_tag_id, choice.fear_tag.tag_weight)
        return answer

    async def get_history(self, user_id: int): return await self.repo.get_user_answers(user_id)
    async def get_avoid_tags(self, user_id: int, include_deleted: bool = False):
        return await self.repo.get_user_fear_tags(user_id, include_deleted=include_deleted)

    async def soft_remove_tag(self, user_id: int, tag_id: int):
        success = await self.repo.soft_delete_fear_tag(user_id, tag_id)
        if not success: raise NotFoundException("태그 없음")
        return {"message": "삭제 완료"}

    async def restore_tag(self, user_id: int, tag_id: int):
        success = await self.repo.restore_fear_tag(user_id, tag_id)
        if not success: raise NotFoundException("태그 없음")
        return {"message": "복구 완료"}

    async def analyze_unfit_jobs(self, user_id: int) -> dict:
        tags = await self.repo.get_user_fear_tags(user_id, include_deleted=False)
        if not tags: return {"summary": "데이터 없음", "unfit_jobs": [], "advice": ""}
        keywords_str = ", ".join([f"{t.tag.tag_name}({t.accumulated_weight})" for t in tags])
        api_key = os.environ.get("SECRET_KEY", "")
        prompt = f"키워드: [{keywords_str}] 기반 진단 JSON..."
        try:
            async with httpx.AsyncClient(timeout=40) as client:
                resp = await client.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={
                    "model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}
                })
                return json.loads(resp.json()["choices"][0]["message"]["content"])
        except: return {"summary": "에러", "unfit_jobs": [], "advice": ""}

    async def get_keyword_suggestions(self, user_id: int) -> list[dict]:
        all_tags = await self.repo.get_all_fear_tags()
        user_tags = await self.repo.get_user_fear_tags(user_id)
        user_tag_ids = {ut.tag_id for ut in user_tags}
        return [{"tag_id": tag.id, "tag_name": tag.tag_name, "already_in_box": tag.id in user_tag_ids} for tag in all_tags]

    # 💡 [중요] 마지막에 선택 저장할 때 호출되는 함수
    async def add_tag_manually(self, user_id: int, tag_id: int) -> dict:
        tag = await self.repo.get_fear_tag_by_id(tag_id)
        if not tag: raise NotFoundException("해당 태그를 찾을 수 없습니다.")
        # DB에 실제 저장
        await self.repo.upsert_fear_tag(user_id, tag_id, tag.tag_weight)
        return {"message": "저장 완료"}

    async def remove_tag_manually(self, user_id: int, tag_id: int):
        await self.repo.delete_fear_tag(user_id, tag_id)
        return {"message": "삭제 완료"}

    async def generate_ai_scenario(self, user_id: int):
        from app.modules.balance.ai_generator import generate_scenario
        return await generate_scenario(self.db, user_id)

    # 💡 [핵심] 게임 도중엔 저장하지 않음
    async def submit_ai_answer(self, user_id: int, body) -> dict:
        return {"message": "기록 완료"}