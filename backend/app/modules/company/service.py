from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import NotFoundException
from app.modules.company.repository import CompanyRepository
from app.modules.company.schemas import ReviewCreate


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyRepository(db)

    async def get_list(self, keyword: Optional[str] = None):
        return await self.repo.get_list(keyword)

    async def get_detail(self, company_id: int):
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundException("회사를 찾을 수 없습니다.")
        return company

    async def get_reviews(self, company_id: int):
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundException("회사를 찾을 수 없습니다.")
        return await self.repo.get_reviews(company_id)

    async def create_review(self, company_id: int, user_id: int, data: ReviewCreate):
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundException("회사를 찾을 수 없습니다.")
        return await self.repo.create_review(
            company_id=company_id,
            user_id=user_id,
            **data.model_dump(),
        )

    async def get_warning_companies(self):
        companies = await self.repo.get_warning_companies()
        result = []
        for c in companies:
            risk_level = "low"
            blacklist_reason = None
            if c.blacklists:
                risk_level = c.blacklists[0].risk_level
                blacklist_reason = c.blacklists[0].blacklist_reason
            elif c.warning_tags:
                risk_level = "medium"

            result.append({
                "company_id": c.id,
                "company_name": c.company_name,
                "risk_level": risk_level,
                "warning_tags": [wt.tag_label for wt in c.warning_tags],
                "blacklist_reason": blacklist_reason,
            })
        return result

    async def get_blacklist(self):
        return await self.repo.get_blacklist()

    async def report_review(self, reporter_id: int, review_id: int, reason: Optional[str]):
        await self.repo.create_report(reporter_id, review_id, reason)
        return {"message": "신고가 접수되었습니다."}
