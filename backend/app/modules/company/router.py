from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.company.schemas import CompanyOut, ReviewCreate, ReviewOut
from app.modules.company.service import CompanyService
from app.modules.users.router import get_current_user

router = APIRouter(tags=["회사"])

@router.get("/companies", response_model=list[CompanyOut])
async def get_companies(keyword: Optional[str] = Query(None), db: AsyncSession = Depends(get_db)):
    service = CompanyService(db)
    return await service.get_list(keyword)

# 💡 수기 입력용 새 경로
@router.post("/companies/manual/reviews", status_code=201)
async def create_review_manual(
    body: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CompanyService(db)
    # 회사 이름 확인 후 생성
    company = await service.repo.get_by_name(body.company_name)
    if not company:
        company = await service.repo.create_company(body.company_name)
    
    data = body.model_dump()
    data.pop("company_name")
    return await service.repo.create_review(company_id=company.id, user_id=current_user.id, **data)

# 💡 리뷰 삭제 경로
@router.delete("/companies/reviews/{review_id}")
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = CompanyService(db)
    review = await service.repo.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 글만 삭제할 수 있습니다.")
    
    await service.repo.delete_review(review)
    return {"message": "삭제 성공"}

@router.get("/companies/{company_id}/reviews", response_model=list[ReviewOut])
async def get_reviews(company_id: int, db: AsyncSession = Depends(get_db)):
    service = CompanyService(db)
    return await service.get_reviews(company_id)