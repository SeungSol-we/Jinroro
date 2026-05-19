from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.base import Base
from app.db.session import engine


async def init_db() -> None:
    """개발 환경에서 테이블 자동 생성. 프로덕션에서는 Alembic 사용."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
