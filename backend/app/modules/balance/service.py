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

    async def get_scenarios(self):
        return await self.repo.get_all_scenarios()

    async def get_scenario(self, scenario_id: int):
        scenario = await self.repo.get_scenario(scenario_id)
        if not scenario:
            raise NotFoundException("시나리오를 찾을 수 없습니다.")
        return scenario

    async def submit_answer(self, user_id: int, body: AnswerRequest):
        scenario = await self.repo.get_scenario(body.scenario_id)
        if not scenario:
            raise NotFoundException("시나리오를 찾을 수 없습니다.")

        choice = await self.repo.get_choice(body.selected_choice_id)
        if not choice or choice.scenario_id != body.scenario_id:
            raise BadRequestException("해당 시나리오의 선택지가 아닙니다.")

        answer = await self.repo.save_answer(user_id, body.scenario_id, body.selected_choice_id)

        if choice.fear_tag:
            await self.repo.upsert_fear_tag(user_id, choice.fear_tag_id, choice.fear_tag.tag_weight)

        return answer

    async def get_history(self, user_id: int):
        return await self.repo.get_user_answers(user_id)

    async def get_avoid_tags(self, user_id: int, include_deleted: bool = False):
        return await self.repo.get_user_fear_tags(user_id, include_deleted=include_deleted)

    async def soft_remove_tag(self, user_id: int, tag_id: int):
        success = await self.repo.soft_delete_fear_tag(user_id, tag_id)
        if not success:
            raise NotFoundException("보관함에 기재된 키워드가 없습니다.")
        return {"message": "휴지통으로 이동되었습니다."}

    # 💡 [교정] 오타(키ware) 및 중복 임포트 구문 정리
    async def restore_tag(self, user_id: int, tag_id: int):
        success = await self.repo.restore_fear_tag(user_id, tag_id)
        if not success:
            raise NotFoundException("휴지통에서 해당 키워드를 찾을 수 없습니다.")
        return {"message": "보관함으로 성공적으로 복구되었습니다."}

    async def analyze_unfit_jobs(self, user_id: int) -> dict:
        tags = await self.repo.get_user_fear_tags(user_id, include_deleted=False)
        if not tags:
            # 💡 스키마 에러를 방지하기 위해 예외 처리를 하거나 규격에 맞는 폴백 오브젝트 반환
            return {
                "summary": "분석할 싫음 키워드가 없습니다.",
                "unfit_jobs": [{"job_title": "미진단", "reason": "밸런스 게임을 먼저 진행해 주세요."}],
                "advice": "게임을 플레이하여 싫어하는 성향을 축적하세요."
            }
        
        keywords_str = ", ".join([f"{t.tag.tag_name}(기피도:{t.accumulated_weight})" for t in tags])
        
        OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
        api_key = os.environ.get("SECRET_KEY", "")
        
        prompt = f"""
        사용자가 가장 싫어하고 기피하는 일자리 특성 키워드 리스트입니다: [{keywords_str}]
        이 데이터들을 기반으로, 이 사람과 '가장 맞지 않는 최악의 일자리 환경/직업군 top 2'를 선별하고 진단해줘.
        
        반드시 다음 JSON 템플릿 형태로만 출력해 텍스트 서론 생략해:
        {{
            "summary": "전체적인 기피 성향 요약 요약문 (한 줄)",
            "unfit_jobs": [
                {{
                    "job_title": "최악의 직업명 1",
                    "reason": "왜 이 키워드를 가진 사람에게 이 직업이 파멸적인지 구체적인 이유 설명"
                }},
                {{
                    "job_title": "최악의 직업명 2",
                    "reason": "왜 이 키워드를 가진 사람에게 이 직업이 지옥인지 구체적인 이유 설명"
                }}
            ],
            "advice": "이러한 환경을 피하기 위해 구직 시 필수로 확인해야 할 팁 한 줄"
        }}
        """
        
        try:
            async with httpx.AsyncClient(timeout=40) as client:
                resp = await client.post(
                    OPENAI_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.7,
                    }
                )
                result_data = resp.json()
                return json.loads(result_data["choices"][0]["message"]["content"])
        except Exception as e:
            return {
                "summary": "성향 분석 연동 중 일시적 지연이 발생했습니다.",
                "unfit_jobs": [{"job_title": "데이터 분석 실패", "reason": f"백엔드 에러 발생: {str(e)}"}],
                "advice": "잠시 후 다시 시도해 주세요."
            }

    async def get_keyword_suggestions(self, user_id: int) -> list[dict]:
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
        tag = await self.repo.get_fear_tag_by_id(tag_id)
        if not tag:
            raise NotFoundException("존재하지 않는 태그입니다.")
        await self.repo.upsert_fear_tag(user_id, tag_id, tag.tag_weight)
        return {"tag_id": tag_id, "tag_name": tag.tag_name, "message": "싫음 보관함에 추가되었습니다."}

    async def remove_tag_manually(self, user_id: int, tag_id: int) -> dict:
        deleted = await self.repo.delete_fear_tag(user_id, tag_id)
        if not deleted:
            raise NotFoundException("싫음 보관함에 해당 태그가 없습니다.")
        return {"tag_id": tag_id, "message": "싫음 보관함에서 제거되었습니다."}

    async def generate_ai_scenario(self, user_id: int) -> dict:
        from app.modules.balance.ai_generator import generate_scenario
        result = await generate_scenario(self.db, user_id)
        if not result:
            raise BadRequestException("시나리오를 생성할 수 없습니다. 배경 테마 또는 태그 데이터를 확인해주세요.")
        return result

    async def submit_ai_answer(self, user_id: int, body) -> dict:
        if body.selected_label not in ("left", "right"):
            raise BadRequestException("selected_label은 'left' 또는 'right'여야 합니다.")

        ai_scenario = await self.repo.get_ai_scenario(body.ai_scenario_id)
        if not ai_scenario:
            raise NotFoundException("AI 시나리오를 찾을 수 없습니다.")

        expected_tag_id = (
            ai_scenario.fear_tag_left_id
            if body.selected_label == "left"
            else ai_scenario.fear_tag_right_id
        )
        if body.selected_fear_tag_id != expected_tag_id:
            raise BadRequestException("선택한 태그 ID가 시나리오와 일치하지 않습니다.")

        tag = await self.repo.get_fear_tag_by_id(body.selected_fear_tag_id)
        if tag:
            await self.repo.upsert_fear_tag(user_id, tag.id, tag.tag_weight)

        return {
            "message": "답변이 저장되었습니다.",
            "added_to_box": tag.tag_name if tag else None,
        }