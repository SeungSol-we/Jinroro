"""
추천 점수 계산 모듈

기획서 기준:
  final_score = base_score - penalty_score + bonus_score + portfolio_match - company_risk_penalty
"""

# 직무별 태그 페널티 맵핑
# { 직무명: { 태그명: 페널티_가중치 } }
JOB_TAG_PENALTY_MAP: dict[str, dict[str, float]] = {
    "IT/소프트웨어": {
        "야근": 1.5,
        "혼자일하기": 0.5,
        "창의성요구": 0.3,
    },
    "품질관리": {
        "반복업무": 0.3,    # 반복 많지만 패널티 낮음 (적성에 맞을 수도 있음)
        "야근": 0.5,
        "육체노동": 0.8,
    },
    "영업/마케팅": {
        "강한대인응대": 2.0,
        "외근많음": 1.5,
        "혼자일하기": 1.0,
    },
    "제조/생산": {
        "반복업무": 1.5,
        "육체노동": 1.5,
        "야근": 1.0,
    },
    "연구개발": {
        "팀협업": 0.5,
        "창의성요구": 0.8,
        "혼자일하기": 1.2,
    },
    "사무/행정": {
        "반복업무": 0.8,
        "강한위계질서": 0.5,
    },
    "전기/전자": {
        "야근": 0.8,
        "육체노동": 0.5,
    },
    "기계/설비": {
        "육체노동": 1.5,
        "야근": 0.8,
    },
    "물류/유통": {
        "육체노동": 1.2,
        "반복업무": 0.8,
        "야근": 1.0,
    },
    "디자인": {
        "창의성요구": 1.0,
        "야근": 1.2,
    },
}

BASE_SCORE = 100.0


def calculate_job_score(
    job_name: str,
    user_fear_tags: list[dict],  # [{"tag_name": str, "accumulated_weight": float}]
    portfolio_match: float = 0.0,
    company_risk_penalty: float = 0.0,
) -> dict:
    """
    단일 직무에 대한 추천 점수 계산

    Args:
        job_name: 직무명
        user_fear_tags: 사용자의 싫음 보관함
        portfolio_match: 포트폴리오 보너스 점수 (0~20)
        company_risk_penalty: 위험 회사 페널티 (0~30)

    Returns:
        {"job_name": str, "score": float, "reason": str}
    """
    penalty_map = JOB_TAG_PENALTY_MAP.get(job_name, {})
    penalty_score = 0.0
    penalty_reasons = []

    for fear in user_fear_tags:
        tag_name = fear["tag_name"]
        user_weight = fear["accumulated_weight"]
        job_penalty_weight = penalty_map.get(tag_name, 0.0)

        if job_penalty_weight > 0:
            penalty = user_weight * job_penalty_weight * 5  # 최대 감점 조정
            penalty_score += penalty
            penalty_reasons.append(f"{tag_name} 성향 불일치")

    final_score = max(0, BASE_SCORE - penalty_score + portfolio_match - company_risk_penalty)

    reason = "적합 가능성 높음"
    if penalty_reasons:
        reason = ", ".join(penalty_reasons[:2])
        if len(penalty_reasons) > 2:
            reason += f" 외 {len(penalty_reasons) - 2}건"

    return {
        "job_name": job_name,
        "score": round(final_score, 1),
        "reason": reason,
    }


def calculate_portfolio_bonus(
    gpa: float | None,
    gpa_max: float,
    cert_count: int,
    award_count: int,
) -> float:
    """포트폴리오 보너스 점수 계산 (최대 20점)"""
    bonus = 0.0

    if gpa and gpa_max > 0:
        ratio = gpa / gpa_max
        bonus += ratio * 8  # GPA 최대 8점

    bonus += min(cert_count * 2, 6)   # 자격증 최대 6점
    bonus += min(award_count * 2, 6)  # 수상 최대 6점

    return round(min(bonus, 20.0), 1)
