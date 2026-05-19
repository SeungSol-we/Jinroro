from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.users.models import UserAward, UserCertification, UserProfile, UserScore


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile(self, user_id: int) -> Optional[UserProfile]:
        result = await self.db.execute(
            select(UserProfile)
            .where(UserProfile.user_id == user_id)
            .options(
                selectinload(UserProfile.certifications),
                selectinload(UserProfile.awards),
            )
        )
        return result.scalar_one_or_none()

    async def upsert_profile(self, user_id: int, **kwargs) -> UserProfile:
        profile = await self.get_profile(user_id)
        if not profile:
            profile = UserProfile(user_id=user_id, **kwargs)
            self.db.add(profile)
        else:
            for k, v in kwargs.items():
                if v is not None:
                    setattr(profile, k, v)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def add_certification(self, profile_id: int, cert_name: str, issued_at: Optional[str]) -> UserCertification:
        cert = UserCertification(profile_id=profile_id, cert_name=cert_name, issued_at=issued_at)
        self.db.add(cert)
        await self.db.flush()
        return cert

    async def add_award(self, profile_id: int, award_name: str, award_level: Optional[str], awarded_at: Optional[str]) -> UserAward:
        award = UserAward(profile_id=profile_id, award_name=award_name, award_level=award_level, awarded_at=awarded_at)
        self.db.add(award)
        await self.db.flush()
        return award

    async def upsert_score(self, user_id: int, gpa: Optional[float], gpa_max: float, description: Optional[str]) -> UserScore:
        result = await self.db.execute(select(UserScore).where(UserScore.user_id == user_id))
        score = result.scalar_one_or_none()
        if not score:
            score = UserScore(user_id=user_id, gpa=gpa, gpa_max=gpa_max, description=description)
            self.db.add(score)
        else:
            score.gpa = gpa
            score.gpa_max = gpa_max
            score.description = description
        await self.db.flush()
        return score
