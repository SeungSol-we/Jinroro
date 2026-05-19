from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=True)
    school: Mapped[str] = mapped_column(String(100), nullable=True)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    certifications: Mapped[list["UserCertification"]] = relationship(back_populates="profile", cascade="all, delete-orphan")
    awards: Mapped[list["UserAward"]] = relationship(back_populates="profile", cascade="all, delete-orphan")


class UserCertification(Base):
    __tablename__ = "user_certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"))
    cert_name: Mapped[str] = mapped_column(String(100), nullable=False)
    issued_at: Mapped[str] = mapped_column(String(20), nullable=True)  # "2024-03" 형식

    profile: Mapped["UserProfile"] = relationship(back_populates="certifications")


class UserAward(Base):
    __tablename__ = "user_awards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"))
    award_name: Mapped[str] = mapped_column(String(150), nullable=False)
    award_level: Mapped[str] = mapped_column(String(50), nullable=True)  # "금상", "장려상" 등
    awarded_at: Mapped[str] = mapped_column(String(20), nullable=True)

    profile: Mapped["UserProfile"] = relationship(back_populates="awards")


class UserScore(Base):
    """학업 성적 / GPA"""
    __tablename__ = "user_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    gpa: Mapped[float] = mapped_column(Float, nullable=True)
    gpa_max: Mapped[float] = mapped_column(Float, default=4.5)
    description: Mapped[str] = mapped_column(Text, nullable=True)
