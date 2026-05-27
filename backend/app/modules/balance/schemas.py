from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FearTagOut(BaseModel):
    id: int
    tag_name: str
    tag_weight: float
    description: Optional[str]

    class Config:
        from_attributes = True


class ChoiceOut(BaseModel):
    id: int
    choice_label: str
    choice_text: str
    fear_tag: Optional[FearTagOut]

    class Config:
        from_attributes = True


class ScenarioOut(BaseModel):
    id: int
    scenario_title: str
    scenario_description: Optional[str]
    choices: list[ChoiceOut]

    class Config:
        from_attributes = True


class AnswerRequest(BaseModel):
    scenario_id: int
    selected_choice_id: int


class AnswerOut(BaseModel):
    id: int
    scenario_id: int
    selected_choice_id: int
    answered_at: datetime

    class Config:
        from_attributes = True


class AvoidTagOut(BaseModel):
    id: int
    tag_id: int
    tag_name: str
    accumulated_weight: float
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TrashTagOut(BaseModel):
    id: int
    tag_id: int
    tag_name: str
    accumulated_weight: float
    description: Optional[str] = None

    class Config:
        from_attributes = True


class KeywordSuggestionOut(BaseModel):
    """게임 완료 후 프론트에 제안할 성격 키워드 목록"""
    tag_id: int
    tag_name: str
    description: Optional[str]
    already_in_box: bool


class ManualTagRequest(BaseModel):
    tag_id: int


class ManualTagDeleteRequest(BaseModel):
    tag_id: int


class AiAnswerRequest(BaseModel):
    ai_scenario_id: int
    selected_label: str        # "left" | "right"
    selected_fear_tag_id: int


class AiScenarioOut(BaseModel):
    ai_scenario_id: Optional[int]
    scenario_title: str
    scenario_description: str
    choices: list[dict]


# ── AI 싫음 기반 직업 분석 리포트 응답 스키마 ──
class UnfitJobDetail(BaseModel):
    job_title: str
    reason: str


class JobAnalysisOut(BaseModel):
    summary: str
    unfit_jobs: list[UnfitJobDetail]
    advice: str