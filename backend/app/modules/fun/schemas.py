from typing import Optional
from pydantic import BaseModel


class FortuneRequest(BaseModel):
    birth_date: Optional[str] = None  # "2006-03-15"


class FaceReadingRequest(BaseModel):
    description: Optional[str] = None  # 사용자가 직접 입력한 관상 특징


class FunResultOut(BaseModel):
    result_text: str
