from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.modules.auth.router import router as auth_router
from app.modules.balance.router import router as balance_router
from app.modules.company.router import router as company_router
from app.modules.fun.router import router as fun_router
from app.modules.recommend.router import router as recommend_router
from app.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 개발 환경에서만 자동 테이블 생성
    if settings.APP_ENV == "development":
        await init_db()
    yield


app = FastAPI(
    title="CareerNoBox API",
    description="싫음보관함 기반 진로/취업 추천 플랫폼",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 프론트엔드 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(balance_router)
app.include_router(recommend_router)
app.include_router(company_router)
app.include_router(fun_router)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.APP_ENV}
