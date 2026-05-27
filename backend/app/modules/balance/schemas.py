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
    tag_name: str
    accumulated_weight: float

    class Config:
        from_attributes = True


class KeywordSuggestionOut(BaseModel):
    """게임 완료 후 프론트에 제안할 성격 키워드 목록"""
    tag_id: int
    tag_name: str
    description: Optional[str]
    already_in_box: bool  # 이미 싫음 보관함에 있는지 여부


class ManualTagRequest(BaseModel):
    """사용자가 직접 싫음 보관함에 태그 추가"""
    tag_id: int


class ManualTagDeleteRequest(BaseModel):
    """사용자가 직접 싫음 보관함에서 태그 제거"""
    tag_id: int


class AiAnswerRequest(BaseModel):
    """AI 생성 시나리오 답변 제출"""
    ai_scenario_id: int        # AiGeneratedScenario.id
    selected_label: str        # "left" | "right"
    selected_fear_tag_id: int  # 선택한 쪽의 fear_tag_id


class AiScenarioOut(BaseModel):
    ai_scenario_id: Optional[int]
    scenario_title: str
    scenario_description: str
    choices: list[dict]
