from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.balance.models import BalanceChoice, BalanceScenario, UserBalanceAnswer, UserFearTag


class BalanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_scenarios(self) -> list[BalanceScenario]:
        result = await self.db.execute(
            select(BalanceScenario)
            .order_by(BalanceScenario.order_num)
            .options(
                selectinload(BalanceScenario.choices).selectinload(BalanceChoice.fear_tag)
            )
        )
        return list(result.scalars().all())

    async def get_scenario(self, scenario_id: int) -> Optional[BalanceScenario]:
        result = await self.db.execute(
            select(BalanceScenario)
            .where(BalanceScenario.id == scenario_id)
            .options(
                selectinload(BalanceScenario.choices).selectinload(BalanceChoice.fear_tag)
            )
        )
        return result.scalar_one_or_none()

    async def get_choice(self, choice_id: int) -> Optional[BalanceChoice]:
        result = await self.db.execute(
            select(BalanceChoice)
            .where(BalanceChoice.id == choice_id)
            .options(selectinload(BalanceChoice.fear_tag))
        )
        return result.scalar_one_or_none()

    async def save_answer(self, user_id: int, scenario_id: int, choice_id: int) -> UserBalanceAnswer:
        # 이미 답변한 시나리오면 업데이트
        result = await self.db.execute(
            select(UserBalanceAnswer).where(
                UserBalanceAnswer.user_id == user_id,
                UserBalanceAnswer.scenario_id == scenario_id,
            )
        )
        answer = result.scalar_one_or_none()
        if answer:
            answer.selected_choice_id = choice_id
        else:
            answer = UserBalanceAnswer(user_id=user_id, scenario_id=scenario_id, selected_choice_id=choice_id)
            self.db.add(answer)
        await self.db.flush()
        return answer

    async def get_user_answers(self, user_id: int) -> list[UserBalanceAnswer]:
        result = await self.db.execute(
            select(UserBalanceAnswer)
            .where(UserBalanceAnswer.user_id == user_id)
            .options(
                selectinload(UserBalanceAnswer.selected_choice).selectinload(BalanceChoice.fear_tag)
            )
        )
        return list(result.scalars().all())

    async def get_user_fear_tags(self, user_id: int) -> list[UserFearTag]:
        result = await self.db.execute(
            select(UserFearTag)
            .where(UserFearTag.user_id == user_id)
            .options(selectinload(UserFearTag.tag))
            .order_by(UserFearTag.accumulated_weight.desc())
        )
        return list(result.scalars().all())

    async def upsert_fear_tag(self, user_id: int, tag_id: int, weight: float):
        result = await self.db.execute(
            select(UserFearTag).where(
                UserFearTag.user_id == user_id,
                UserFearTag.tag_id == tag_id,
            )
        )
        user_tag = result.scalar_one_or_none()
        if user_tag:
            user_tag.accumulated_weight += weight
        else:
            user_tag = UserFearTag(user_id=user_id, tag_id=tag_id, accumulated_weight=weight)
            self.db.add(user_tag)
        await self.db.flush()
