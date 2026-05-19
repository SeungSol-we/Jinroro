from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import RiskLevel
from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    employee_count: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    reviews: Mapped[list["CompanyReview"]] = relationship(back_populates="company", cascade="all, delete-orphan")
    blacklists: Mapped[list["CompanyBlacklist"]] = relationship(back_populates="company")
    warning_tags: Mapped[list["CompanyWarningTag"]] = relationship(back_populates="company")


class CompanyReview(Base):
    __tablename__ = "company_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)

    # 평가 항목 (1~5점)
    work_life_balance_score: Mapped[float] = mapped_column(Float, nullable=True)
    salary_satisfaction_score: Mapped[float] = mapped_column(Float, nullable=True)
    growth_score: Mapped[float] = mapped_column(Float, nullable=True)
    management_score: Mapped[float] = mapped_column(Float, nullable=True)

    # 텍스트
    content: Mapped[str] = mapped_column(Text, nullable=True)
    resignation_reason: Mapped[str] = mapped_column(Text, nullable=True)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)  # 신고로 숨김
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="reviews")


class CompanyBlacklist(Base):
    """공개 체불사업주 등 공공 데이터 기반 위험 정보"""
    __tablename__ = "company_blacklists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    blacklist_reason: Mapped[str] = mapped_column(String(300), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default=RiskLevel.HIGH)
    public_source: Mapped[str] = mapped_column(String(200), nullable=True)   # "고용노동부 체불사업주 공개명단"
    evidence_url: Mapped[str] = mapped_column(String(500), nullable=True)
    reported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="blacklists")


class CompanyWarningTag(Base):
    """주의 태그 (임금체불 위험, 후기 부정 다수 등)"""
    __tablename__ = "company_warning_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    tag_label: Mapped[str] = mapped_column(String(100), nullable=False)  # "임금체불 위험"

    company: Mapped["Company"] = relationship(back_populates="warning_tags")


class ReportLog(Base):
    """후기 신고 로그"""
    __tablename__ = "report_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reporter_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    review_id: Mapped[int] = mapped_column(Integer, ForeignKey("company_reviews.id"))
    reason: Mapped[str] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
