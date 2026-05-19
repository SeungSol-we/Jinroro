from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.company.models import Company, CompanyBlacklist, CompanyReview, CompanyWarningTag, ReportLog


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, keyword: Optional[str] = None) -> list[Company]:
        query = select(Company)
        if keyword:
            query = query.where(Company.company_name.ilike(f"%{keyword}%"))
        result = await self.db.execute(query.order_by(Company.company_name))
        return list(result.scalars().all())

    async def get_by_id(self, company_id: int) -> Optional[Company]:
        result = await self.db.execute(
            select(Company)
            .where(Company.id == company_id)
            .options(
                selectinload(Company.warning_tags),
                selectinload(Company.blacklists),
            )
        )
        return result.scalar_one_or_none()

    async def get_reviews(self, company_id: int) -> list[CompanyReview]:
        result = await self.db.execute(
            select(CompanyReview)
            .where(CompanyReview.company_id == company_id, CompanyReview.is_hidden == False)
            .order_by(CompanyReview.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_review(self, company_id: int, user_id: int, **kwargs) -> CompanyReview:
        review = CompanyReview(company_id=company_id, user_id=user_id, **kwargs)
        self.db.add(review)
        await self.db.flush()
        return review

    async def get_warning_companies(self) -> list[Company]:
        """블랙리스트 또는 경고 태그가 있는 회사 목록"""
        result = await self.db.execute(
            select(Company)
            .join(CompanyBlacklist, isouter=True)
            .join(CompanyWarningTag, isouter=True)
            .options(
                selectinload(Company.blacklists),
                selectinload(Company.warning_tags),
            )
            .distinct()
        )
        return list(result.scalars().all())

    async def get_blacklist(self) -> list[CompanyBlacklist]:
        result = await self.db.execute(
            select(CompanyBlacklist)
            .options(selectinload(CompanyBlacklist.company))
            .order_by(CompanyBlacklist.reported_at.desc())
        )
        return list(result.scalars().all())

    async def create_report(self, reporter_id: int, review_id: int, reason: Optional[str]):
        report = ReportLog(reporter_user_id=reporter_id, review_id=review_id, reason=reason)
        self.db.add(report)
        await self.db.flush()
