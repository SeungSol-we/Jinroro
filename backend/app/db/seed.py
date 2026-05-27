"""
초기 데이터 시딩 스크립트

실행:
  docker-compose exec api python -m app.db.seed
"""

import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.modules.balance.models import FearTag

FEAR_TAGS = [
    {"tag_name": "야근",         "tag_weight": 1.5, "description": "퇴근 시간 이후에도 일해야 하는 환경"},
    {"tag_name": "반복업무",      "tag_weight": 1.2, "description": "매일 똑같은 작업이 반복되는 업무"},
    {"tag_name": "강한대인응대",   "tag_weight": 1.3, "description": "고객/외부인과 잦은 대화가 필요한 업무"},
    {"tag_name": "외근많음",      "tag_weight": 1.0, "description": "사무실보다 외부에서 보내는 시간이 많음"},
    {"tag_name": "육체노동",      "tag_weight": 1.2, "description": "신체를 많이 사용하는 작업"},
    {"tag_name": "혼자일하기",    "tag_weight": 1.0, "description": "팀보다 혼자 업무를 처리하는 비중이 높음"},
    {"tag_name": "팀협업",       "tag_weight": 1.0, "description": "여러 사람과 긴밀하게 협력해야 하는 환경"},
    {"tag_name": "높은책임감",    "tag_weight": 1.3, "description": "중요한 결정이나 큰 책임을 지는 역할"},
    {"tag_name": "창의성요구",    "tag_weight": 1.1, "description": "새로운 아이디어나 창의적 사고가 필요한 업무"},
    {"tag_name": "강한위계질서",  "tag_weight": 1.2, "description": "상하관계가 뚜렷하고 보고 체계가 복잡한 조직"},
]


async def seed():
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(FearTag))
        if not existing.scalars().all():
            for data in FEAR_TAGS:
                db.add(FearTag(**data))
            await db.commit()
            print(f"✅ FearTag {len(FEAR_TAGS)}개 추가 완료")
        else:
            print("ℹ️  FearTag 이미 존재 - 스킵")


if __name__ == "__main__":
    asyncio.run(seed())
