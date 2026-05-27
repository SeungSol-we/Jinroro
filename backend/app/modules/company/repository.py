from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.company.models import Company, CompanyReview

class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, keyword: Optional[str] = None):
        query = select(Company)
        if keyword:
            query = query.where(Company.company_name.ilike(f"%{keyword}%"))
        result = await self.db.execute(query.order_by(Company.company_name))
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Optional[Company]:
        result = await self.db.execute(select(Company).where(Company.company_name == name))
        return result.scalar_one_or_none()

    async def create_company(self, name: str) -> Company:
        company = Company(company_name=name)
        self.db.add(company)
        await self.db.flush()
        return company

    async def get_review_by_id(self, review_id: int) -> Optional[CompanyReview]:
        result = await self.db.execute(select(CompanyReview).where(CompanyReview.id == review_id))
        return result.scalar_one_or_none()

    async def delete_review(self, review: CompanyReview):
        await self.db.delete(review)
        await self.db.flush()

    async def get_reviews(self, company_id: int):
        result = await self.db.execute(
            select(CompanyReview)
            .where(CompanyReview.company_id == company_id, CompanyReview.is_hidden == False)
            .order_by(CompanyReview.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_review(self, company_id: int, user_id: int, **kwargs):
        review = CompanyReview(company_id=company_id, user_id=user_id, **kwargs)
        self.db.add(review)
        await self.db.flush()
        await self.db.refresh(review)
        return review