from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.balance.repository import BalanceRepository
from app.modules.users.models import UserCertification, UserAward, UserScore, UserProfile
from app.utils.score_calculator import JOB_TAG_PENALTY_MAP, calculate_job_score, calculate_portfolio_bonus


class RecommendService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.balance_repo = BalanceRepository(db)

    async def get_result(self, user_id: int) -> dict:
        # 1. 싫음 태그 수집
        fear_tags_orm = await self.balance_repo.get_user_fear_tags(user_id)
        fear_tags = [
            {"tag_name": t.tag.tag_name, "accumulated_weight": t.accumulated_weight}
            for t in fear_tags_orm
        ]

        # 2. 포트폴리오 정보 수집
        profile_result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = profile_result.scalar_one_or_none()

        score_result = await self.db.execute(
            select(UserScore).where(UserScore.user_id == user_id)
        )
        user_score = score_result.scalar_one_or_none()

        cert_count = 0
        award_count = 0
        if profile:
            cert_result = await self.db.execute(
                select(UserCertification).where(UserCertification.profile_id == profile.id)
            )
            cert_count = len(cert_result.scalars().all())

            award_result = await self.db.execute(
                select(UserAward).where(UserAward.profile_id == profile.id)
            )
            award_count = len(award_result.scalars().all())

        portfolio_bonus = calculate_portfolio_bonus(
            gpa=user_score.gpa if user_score else None,
            gpa_max=user_score.gpa_max if user_score else 4.5,
            cert_count=cert_count,
            award_count=award_count,
        )

        # 3. 전체 직무 점수 계산 후 정렬
        all_jobs = list(JOB_TAG_PENALTY_MAP.keys())
        job_scores = [
            calculate_job_score(job, fear_tags, portfolio_bonus)
            for job in all_jobs
        ]
        job_scores.sort(key=lambda x: x["score"], reverse=True)

        return {
            "user_id": user_id,
            "avoid_tags": [t["tag_name"] for t in fear_tags],
            "recommended_jobs": job_scores,
            "portfolio_bonus": portfolio_bonus,
        }
