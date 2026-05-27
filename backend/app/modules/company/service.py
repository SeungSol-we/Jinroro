from app.modules.company.repository import CompanyRepository
from app.modules.company.schemas import ReviewCreate

class CompanyService:
    def __init__(self, db):
        self.repo = CompanyRepository(db)

    async def get_list(self, keyword=None):
        return await self.repo.get_list(keyword)

    async def get_reviews(self, company_id):
        return await self.repo.get_reviews(company_id)

    # 💡 자동 생성 로직 포함된 리뷰 생성 함수
    async def create_review_auto(self, user_id, data: ReviewCreate):
        # 1. 이름으로 회사 검색
        company = await self.repo.get_by_name(data.company_name)
        # 2. 없으면 생성
        if not company:
            company = await self.repo.create_company(data.company_name)
        
        # 3. 리뷰 데이터 준비 (이름 필드 제외)
        review_dict = data.model_dump()
        review_dict.pop("company_name")
        
        return await self.repo.create_review(
            company_id=company.id,
            user_id=user_id,
            **review_dict
        )