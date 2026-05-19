from typing import Optional
from pydantic import BaseModel


class JobRecommendOut(BaseModel):
    job_name: str
    score: float
    reason: str


class RecommendResultOut(BaseModel):
    user_id: int
    avoid_tags: list[str]
    recommended_jobs: list[JobRecommendOut]
    portfolio_bonus: float
