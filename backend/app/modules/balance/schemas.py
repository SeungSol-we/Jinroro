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
