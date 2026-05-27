from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FearTag(Base):
    """싫음 태그 마스터 데이터 (야근, 반복업무 등)"""
    __tablename__ = "fear_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tag_weight: Mapped[float] = mapped_column(Float, default=1.0)
    description: Mapped[str] = mapped_column(String(200), nullable=True)


class BalanceScenario(Base):
    """수동으로 등록한 고정 시나리오"""
    __tablename__ = "balance_scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_title: Mapped[str] = mapped_column(String(200), nullable=False)
    scenario_description: Mapped[str] = mapped_column(Text, nullable=True)
    order_num: Mapped[int] = mapped_column(Integer, default=0)

    choices: Mapped[list["BalanceChoice"]] = relationship(back_populates="scenario", cascade="all, delete-orphan")


class BalanceChoice(Base):
    __tablename__ = "balance_choices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(Integer, ForeignKey("balance_scenarios.id", ondelete="CASCADE"))
    choice_label: Mapped[str] = mapped_column(String(10), nullable=False)
    choice_text: Mapped[str] = mapped_column(String(300), nullable=False)
    fear_tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("fear_tags.id"), nullable=True)

    scenario: Mapped["BalanceScenario"] = relationship(back_populates="choices")
    fear_tag: Mapped[FearTag] = relationship()


class UserBalanceAnswer(Base):
    __tablename__ = "user_balance_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    scenario_id: Mapped[int] = mapped_column(Integer, ForeignKey("balance_scenarios.id"))
    selected_choice_id: Mapped[int] = mapped_column(Integer, ForeignKey("balance_choices.id"))
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    scenario: Mapped["BalanceScenario"] = relationship()
    selected_choice: Mapped["BalanceChoice"] = relationship()


class UserFearTag(Base):
    """사용자의 싫음 보관함"""
    __tablename__ = "user_fear_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("fear_tags.id"))
    accumulated_weight: Mapped[float] = mapped_column(Float, default=1.0)
    # 💡 [추가] 휴지통 관리를 위한 플래그 필드 추가
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tag: Mapped[FearTag] = relationship()


class AiGeneratedScenario(Base):
    """AI가 생성한 시나리오 캐시"""
    __tablename__ = "ai_generated_scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fear_tag_left_id: Mapped[int] = mapped_column(Integer, ForeignKey("fear_tags.id"), nullable=True)
    fear_tag_right_id: Mapped[int] = mapped_column(Integer, ForeignKey("fear_tags.id"), nullable=True)

    scenario_title: Mapped[str] = mapped_column(String(300), nullable=False)
    scenario_description: Mapped[str] = mapped_column(Text, nullable=False)
    choice_left_text: Mapped[str] = mapped_column(String(400), nullable=False)
    choice_right_text: Mapped[str] = mapped_column(String(400), nullable=False)
    keyword_left: Mapped[str] = mapped_column(String(50), nullable=True)
    keyword_right: Mapped[str] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fear_tag_left: Mapped["FearTag"] = relationship(foreign_keys=[fear_tag_left_id])
    fear_tag_right: Mapped["FearTag"] = relationship(foreign_keys=[fear_tag_right_id])
