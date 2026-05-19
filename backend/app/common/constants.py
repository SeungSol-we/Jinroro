from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class JobCategory(str, Enum):
    IT = "IT/소프트웨어"
    MANUFACTURING = "제조/생산"
    QUALITY = "품질관리"
    ELECTRICAL = "전기/전자"
    MECHANICAL = "기계/설비"
    LOGISTICS = "물류/유통"
    SALES = "영업/마케팅"
    ADMIN = "사무/행정"
    DESIGN = "디자인"
    RESEARCH = "연구개발"


class AvoidTagType(str, Enum):
    OVERTIME = "야근"
    REPETITIVE = "반복업무"
    INTERPERSONAL = "강한대인응대"
    OUTDOOR = "외근많음"
    PHYSICAL = "육체노동"
    SOLO_WORK = "혼자일하기"
    TEAM_WORK = "팀협업"
    RESPONSIBILITY = "높은책임감"
    CREATIVITY = "창의성요구"
    STRICT_HIERARCHY = "강한위계질서"
