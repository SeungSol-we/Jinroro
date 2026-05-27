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

    async def get_user_fear_tags(self, user_id: int, include_deleted: bool = False) -> list[UserFearTag]:
        result = await self.db.execute(
            select(UserFearTag)
            .where(UserFearTag.user_id == user_id, UserFearTag.is_deleted == include_deleted)
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
            user_tag.is_deleted = False  # 재누적 시 휴지통에서 자동 탈출
        else:
            user_tag = UserFearTag(user_id=user_id, tag_id=tag_id, accumulated_weight=weight, is_deleted=False)
            self.db.add(user_tag)
        await self.db.flush()

    async def soft_delete_fear_tag(self, user_id: int, tag_id: int) -> bool:
        result = await self.db.execute(
            select(UserFearTag).where(UserFearTag.user_id == user_id, UserFearTag.tag_id == tag_id, UserFearTag.is_deleted == False)
        )
        user_tag = result.scalar_one_or_none()
        if not user_tag:
            return False
        user_tag.is_deleted = True  # 휴지통으로 이동 플래그
        await self.db.flush()
        return True

    async def restore_fear_tag(self, user_id: int, tag_id: int) -> bool:
        result = await self.db.execute(
            select(UserFearTag).where(UserFearTag.user_id == user_id, UserFearTag.tag_id == tag_id, UserFearTag.is_deleted == True)
        )
        user_tag = result.scalar_one_or_none()
        if not user_tag:
            return False
        user_tag.is_deleted = False  # 보관함으로 복구
        await self.db.flush()
        return True

    async def get_all_fear_tags(self):
        from app.modules.balance.models import FearTag
        result = await self.db.execute(select(FearTag).order_by(FearTag.id))
        return list(result.scalars().all())

    async def get_fear_tag_by_id(self, tag_id: int):
        from app.modules.balance.models import FearTag
        result = await self.db.execute(select(FearTag).where(FearTag.id == tag_id))
        return result.scalar_one_or_none()

    async def get_user_fear_tag(self, user_id: int, tag_id: int) -> Optional[UserFearTag]:
        result = await self.db.execute(
            select(UserFearTag).where(
                UserFearTag.user_id == user_id,
                UserFearTag.tag_id == tag_id,
            )
        )
        return result.scalar_one_or_none()

    async def delete_fear_tag(self, user_id: int, tag_id: int) -> bool:
        user_tag = await self.get_user_fear_tag(user_id, tag_id)
        if not user_tag:
            return False
        await self.db.delete(user_tag)
        await self.db.flush()
        return True

    async def get_ai_scenario(self, ai_scenario_id: int):
        from app.modules.balance.models import AiGeneratedScenario
        result = await self.db.execute(
            select(AiGeneratedScenario).where(AiGeneratedScenario.id == ai_scenario_id)
        )
        return result.scalar_one_or_none()
