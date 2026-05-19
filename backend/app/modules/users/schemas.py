from typing import Optional

from pydantic import BaseModel


class CertificationIn(BaseModel):
    cert_name: str
    issued_at: Optional[str] = None


class AwardIn(BaseModel):
    award_name: str
    award_level: Optional[str] = None
    awarded_at: Optional[str] = None


class UserProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    school: Optional[str] = None
    department: Optional[str] = None
    graduation_year: Optional[int] = None
    bio: Optional[str] = None


class UserScoreUpdate(BaseModel):
    gpa: Optional[float] = None
    gpa_max: Optional[float] = 4.5
    description: Optional[str] = None


class CertificationOut(BaseModel):
    id: int
    cert_name: str
    issued_at: Optional[str]

    class Config:
        from_attributes = True


class AwardOut(BaseModel):
    id: int
    award_name: str
    award_level: Optional[str]
    awarded_at: Optional[str]

    class Config:
        from_attributes = True


class UserProfileOut(BaseModel):
    id: int
    user_id: int
    nickname: Optional[str]
    school: Optional[str]
    department: Optional[str]
    graduation_year: Optional[int]
    bio: Optional[str]
    certifications: list[CertificationOut] = []
    awards: list[AwardOut] = []

    class Config:
        from_attributes = True
