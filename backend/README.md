# CareerNoBox Backend

싫음보관함 기반 진로/취업 추천 플랫폼 백엔드

## 기술 스택
- FastAPI + SQLAlchemy (async)
- PostgreSQL (Docker)
- JWT 인증
- Alembic (마이그레이션)

## 로컬 실행

### 1. 환경변수 설정
```bash
cp .env .env.local  # .env 파일은 이미 기본값으로 설정되어 있음
```

### 2. Docker로 DB + API 실행
```bash
docker-compose up --build
```

### 3. API 문서 확인
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 개발 시 로컬 실행 (Docker 없이 API만)

```bash
# 의존성 설치
pip install -r requirements.txt

# DB는 Docker로만 실행
docker-compose up db -d

# API 실행
uvicorn app.main:app --reload
```

---

## Alembic 마이그레이션

```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "init"

# 마이그레이션 적용
alembic upgrade head
```

> 개발 환경(`APP_ENV=development`)에서는 서버 시작 시 테이블이 자동 생성됨.

---

## API 구조

| 도메인 | 경로 | 설명 |
|--------|------|------|
| 인증 | `/auth/*` | 회원가입, 로그인, 토큰 갱신 |
| 사용자 | `/users/me/*` | 프로필, 자격증, 수상, 성적 |
| 밸런스게임 | `/balance/*` | 시나리오, 답변 제출, 싫음 보관함 |
| 추천 | `/recommend/result` | 직무 추천 결과 |
| 회사 | `/companies/*` | 회사 목록/상세/후기 |
| 위험회사 | `/warnings/*` | 블랙리스트, 주의 회사 |
| 재미 | `/fun/*` | 운세, 관상 |

---

## 폴더 구조

```
app/
├── main.py              # FastAPI 앱 진입점
├── core/                # 설정, 보안(JWT/bcrypt)
├── db/                  # DB 세션, Base, 초기화
├── common/              # 예외, 응답 형식, 상수
├── utils/               # 점수 계산, 태그 매핑
└── modules/
    ├── auth/            # 인증 (회원가입/로그인)
    ├── users/           # 사용자 프로필/포트폴리오
    ├── balance/         # 밸런스게임 + 싫음보관함
    ├── recommend/       # 직무 추천 로직
    ├── company/         # 회사/후기/블랙리스트
    └── fun/             # 사주/관상
```

나중에 추가할 것들 (현재 뼈대만)

fun/service.py → OpenAI API 연동하면 실제 사주/관상 분석 가능
score_calculator.py → 직무별 태그 페널티 맵 데이터 보강 (기획팀이랑 협의)
임금체불 공공 API 크롤링 스크립트 (/warnings/blacklist 에 데이터 채워넣기)
Alembic 마이그레이션 파일 생성 (alembic revision --autogenerate -m "init")