from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CompanyOut(BaseModel):
    id: int
    company_name: str
    industry: Optional[str]
    location: Optional[str]
    employee_count: Optional[int]
    description: Optional[str]
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    company_name: str
    is_anonymous: bool = True
    work_life_balance_score: Optional[float] = Field(None, ge=1, le=5)
    salary_satisfaction_score: Optional[float] = Field(None, ge=1, le=5)
    growth_score: Optional[float] = Field(None, ge=1, le=5)
    management_score: Optional[float] = Field(None, ge=1, le=5)
    content: Optional[str] = None
    resignation_reason: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    user_id: Optional[int] # 💡 삭제 권한 확인용
    is_anonymous: bool
    company_id: int
    content: Optional[str]
    resignation_reason: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class BlacklistOut(BaseModel):
    id: int
    company_id: int
    company_name: str
    blacklist_reason: str
    risk_level: str
    public_source: Optional[str]
    evidence_url: Optional[str]
    reported_at: datetime
    class Config:
        from_attributes = True

class WarningCompanyOut(BaseModel):
    company_id: int
    company_name: str
    risk_level: str
    warning_tags: list[str]
    blacklist_reason: Optional[str]

class ReportCreate(BaseModel):
    reason: Optional[str] = None