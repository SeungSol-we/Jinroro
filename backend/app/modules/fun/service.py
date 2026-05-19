import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.fun.models import FaceReading, FortuneReport

FORTUNE_TEXTS = [
    "오늘은 새로운 가능성이 열리는 날입니다. 도전을 두려워하지 마세요.",
    "꾸준한 노력이 빛을 발하는 시기입니다. 자격증 공부를 시작해보세요.",
    "인간관계에서 좋은 기운이 흐릅니다. 팀 프로젝트에 적극적으로 참여해보세요.",
    "안정을 추구하는 시기입니다. 무리한 도전보다 현재에 충실하세요.",
    "창의성이 빛나는 날입니다. 아이디어를 노트에 기록해보세요.",
]

FACE_READING_TEXTS = [
    "눈빛이 총명하여 분석적인 직무에 어울립니다. IT 계열이 잘 맞을 것 같아요.",
    "단단한 인상에서 책임감이 느껴집니다. 품질관리나 안전 직무가 좋을 것 같아요.",
    "따뜻한 인상으로 사람들과의 협업에 강점이 있어 보입니다.",
    "집중력이 강한 인상입니다. 꼼꼼함이 요구되는 직무에서 빛날 것 같아요.",
]


class FunService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_fortune(self, user_id: int, birth_date: str = None) -> dict:
        result_text = random.choice(FORTUNE_TEXTS)
        report = FortuneReport(user_id=user_id, birth_date=birth_date, result_text=result_text)
        self.db.add(report)
        await self.db.flush()
        return {"result_text": result_text}

    async def get_face_reading(self, user_id: int, description: str = None) -> dict:
        result_text = random.choice(FACE_READING_TEXTS)
        reading = FaceReading(user_id=user_id, result_text=result_text)
        self.db.add(reading)
        await self.db.flush()
        return {"result_text": result_text}
