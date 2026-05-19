from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import NotFoundException
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import AwardIn, CertificationIn, UserProfileUpdate, UserScoreUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_my_profile(self, user_id: int):
        profile = await self.repo.get_profile(user_id)
        if not profile:
            raise NotFoundException("프로필이 없습니다. 먼저 프로필을 생성해주세요.")
        return profile

    async def update_my_profile(self, user_id: int, data: UserProfileUpdate):
        return await self.repo.upsert_profile(user_id, **data.model_dump(exclude_none=True))

    async def add_certification(self, user_id: int, data: CertificationIn):
        profile = await self.repo.get_profile(user_id)
        if not profile:
            profile = await self.repo.upsert_profile(user_id)
        return await self.repo.add_certification(profile.id, data.cert_name, data.issued_at)

    async def add_award(self, user_id: int, data: AwardIn):
        profile = await self.repo.get_profile(user_id)
        if not profile:
            profile = await self.repo.upsert_profile(user_id)
        return await self.repo.add_award(profile.id, data.award_name, data.award_level, data.awarded_at)

    async def update_score(self, user_id: int, data: UserScoreUpdate):
        return await self.repo.upsert_score(user_id, data.gpa, data.gpa_max or 4.5, data.description)
