from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.company.schemas import BlacklistOut, CompanyOut, ReportCreate, ReviewCreate, ReviewOut, WarningCompanyOut
from app.modules.company.service import CompanyService
from app.modules.users.router import get_current_user

router = APIRouter(tags=["회사"])


# ── 회사 목록 / 상세 ──────────────────────────────────────────
@router.get("/companies", response_model=list[CompanyOut])
async def get_companies(
    keyword: Optional[str] = Query(None, description="회사명 검색"),
    db: AsyncSession = Depends(get_db),
):
    service = CompanyService(db)
    return await service.get_list(keyword)


@router.get("/companies/{company_id}", response_model=CompanyOut)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    service = CompanyService(db)
    return await service.get_detail(company_id)


# ── 후기 ──────────────────────────────────────────────────────
@router.get("/companies/{company_id}/reviews", response_model=list[ReviewOut])
async def get_reviews(company_id: int, db: AsyncSession = Depends(get_db)):
    service = CompanyService(db)
    return await service.get_reviews(company_id)


@router.post("/companies/{company_id}/reviews", status_code=201)
async def create_review(
    company_id: int,
    body: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """후기 작성 (익명 가능)"""
    service = CompanyService(db)
    return await service.create_review(company_id, current_user.id, body)


@router.post("/companies/reviews/{review_id}/report", status_code=201)
async def report_review(
    review_id: int,
    body: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """후기 신고"""
    service = CompanyService(db)
    return await service.report_review(current_user.id, review_id, body.reason)


# ── 위험 회사 ──────────────────────────────────────────────────
@router.get("/warnings/companies", response_model=list[WarningCompanyOut])
async def get_warning_companies(db: AsyncSession = Depends(get_db)):
    """주의 회사 목록 (공개 정보 기반)"""
    service = CompanyService(db)
    return await service.get_warning_companies()


@router.get("/warnings/blacklist")
async def get_blacklist(db: AsyncSession = Depends(get_db)):
    """임금체불 등 공개 블랙리스트"""
    service = CompanyService(db)
    items = await service.get_blacklist()
    return [
        {
            "id": b.id,
            "company_id": b.company_id,
            "company_name": b.company.company_name,
            "blacklist_reason": b.blacklist_reason,
            "risk_level": b.risk_level,
            "public_source": b.public_source,
            "evidence_url": b.evidence_url,
            "reported_at": b.reported_at,
        }
        for b in items
    ]
