import json
import os
import random
from typing import Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.balance.models import AiGeneratedScenario, FearTag

# 💡 OpenAI(GPT) 주소 및 모델로 변경
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"  # 혹은 프로젝트 요금제에 맞춰 gpt-4o 등을 지정해 사용하세요.

SYSTEM_PROMPT = """너는 취업 준비생을 위한 진로 탐색 게임의 시나리오 작가야.
병맛스럽고 재밌는 가상의 상황을 만들어서, 플레이어가 두 선택지 중 '더 싫은 것'을 고르게 해야 해.
선택 결과로 그 사람의 직업 성향(야근 싫음, 반복업무 싫음 등)을 파악하는 게 목적이야.

규칙:
- 폭력, 성적 표현, 혐오 표현 절대 금지
- 특정 인물/종교/정치 비하 금지
- 병맛이되 선을 넘지 않는 유머 사용
- 상황은 구체적이고 생생하게 (2~3문장)
- 선택지는 각각 직업 세계의 실제 고통 포인트를 반영
- 반드시 JSON만 반환, 다른 텍스트 없음
- 스토리들은 이전 질문과 연결되도록 해야함
- 현실적인 상황을 바탕으로 질문이 나오도록
"""

USER_PROMPT_TEMPLATE = """왼쪽 선택지가 드러내야 할 직업 성향: {tag_left}
오른쪽 선택지가 드러내야 할 직업 성향: {tag_right}

완전히 자유롭게 상황을 설정해서 병맛 스토리와 선택지를 만들어줘.
플레이어는 "더 싫은 것"을 고르는 거야. 둘 다 괴롭지만 방향이 다른 고통이어야 해.

반드시 아래 JSON 형식으로만 응답해:
{{
  "scenario_title": "한 줄 제목 (20자 이내)",
  "scenario_description": "상황 설명 (2~3문장, 병맛 있게)",
  "choice_left": "왼쪽 선택지 텍스트 (1~2문장)",
  "choice_right": "오른쪽 선택지 텍스트 (1~2문장)",
  "keyword_left": "{tag_left} 성향을 한 단어로",
  "keyword_right": "{tag_right} 성향을 한 단어로"
}}"""


async def generate_scenario(
    db: AsyncSession,
    user_id: int,
) -> Optional[dict]:
    # 1. 전체 fear_tag 목록
    all_tags_result = await db.execute(select(FearTag))
    all_tags = list(all_tags_result.scalars().all())
    if len(all_tags) < 2:
        return None

    # 2. 이미 생성된 태그 조합 제외
    seen_result = await db.execute(
        select(AiGeneratedScenario.fear_tag_left_id, AiGeneratedScenario.fear_tag_right_id)
    )
    seen_pairs = {(r[0], r[1]) for r in seen_result.all()}

    shuffled = random.sample(all_tags, len(all_tags))
    tag_left, tag_right = None, None
    for i, t1 in enumerate(shuffled):
        for t2 in shuffled[i + 1:]:
            if (t1.id, t2.id) not in seen_pairs and (t2.id, t1.id) not in seen_pairs:
                tag_left, tag_right = t1, t2
                break
        if tag_left:
            break

    if not tag_left:
        tag_left, tag_right = random.sample(all_tags, 2)

    # 3. 캐시 조회
    cache_result = await db.execute(
        select(AiGeneratedScenario).where(
            AiGeneratedScenario.fear_tag_left_id == tag_left.id,
            AiGeneratedScenario.fear_tag_right_id == tag_right.id,
        )
    )
    cached = cache_result.scalar_one_or_none()
    if cached:
        return _to_dict(cached)

    # 4. OpenAI API 호출로 변경
    api_key = os.environ.get("SECRET_KEY", "")
    prompt = USER_PROMPT_TEMPLATE.format(
        tag_left=tag_left.tag_name,
        tag_right=tag_right.tag_name,
    )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                OPENAI_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    # 안전하게 JSON 포맷으로 응답하도록 강제
                    "response_format": {"type": "json_object"},
                    "temperature": 0.8,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        # OpenAI Response 구조에 맞춰 텍스트 파싱
        raw_text = data["choices"][0]["message"]["content"].strip()
        parsed = json.loads(raw_text)

    except Exception as e:
        print(f"[AI 생성 실패] {e}")
        return _fallback_scenario(tag_left, tag_right)

    # 5. DB 저장
    ai_scenario = AiGeneratedScenario(
        fear_tag_left_id=tag_left.id,
        fear_tag_right_id=tag_right.id,
        scenario_title=parsed.get("scenario_title", ""),
        scenario_description=parsed.get("scenario_description", ""),
        choice_left_text=parsed.get("choice_left", ""),
        choice_right_text=parsed.get("choice_right", ""),
        keyword_left=parsed.get("keyword_left", tag_left.tag_name),
        keyword_right=parsed.get("keyword_right", tag_right.tag_name),
    )
    db.add(ai_scenario)
    await db.flush()
    await db.refresh(ai_scenario)

    return _to_dict(ai_scenario)


def _to_dict(scenario: AiGeneratedScenario) -> dict:
    return {
        "ai_scenario_id": scenario.id,
        "scenario_title": scenario.scenario_title,
        "scenario_description": scenario.scenario_description,
        "choices": [
            {
                "label": "left",
                "text": scenario.choice_left_text,
                "keyword": scenario.keyword_left,
                "fear_tag_id": scenario.fear_tag_left_id,
            },
            {
                "label": "right",
                "text": scenario.choice_right_text,
                "keyword": scenario.keyword_right,
                "fear_tag_id": scenario.fear_tag_right_id,
            },
        ],
    }


def _fallback_scenario(tag_left, tag_right) -> dict:
    """API 실패 시 폴백 — ai_scenario_id가 None이면 답변 제출 불가하므로 DB에 저장된 척 처리 안 함"""
    return {
        "ai_scenario_id": None,
        "scenario_title": "오늘의 선택",
        "scenario_description": "당신 앞에 두 가지 상황이 펼쳐집니다. 더 싫은 쪽을 골라주세요.",
        "choices": [
            {
                "label": "left",
                "text": f"{tag_left.tag_name} 상황을 감수한다",
                "keyword": tag_left.tag_name,
                "fear_tag_id": tag_left.id,
            },
            {
                "label": "right",
                "text": f"{tag_right.tag_name} 상황을 감수한다",
                "keyword": tag_right.tag_name,
                "fear_tag_id": tag_right.id,
            },
        ],
    }