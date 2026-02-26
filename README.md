# 사주 포트폴리오 리밸런서

사주 명리학과 AI를 결합하여 개인 맞춤형 투자 포트폴리오 리밸런싱을 제안하는 웹 애플리케이션입니다.

생년월일·시진·성별을 입력하면 사주 팔자를 분석하고, 보유 포트폴리오를 자유 형식으로 입력하면 Gemini AI가 사주 풀이를 토대로 맞춤형 리밸런싱 전략을 제시합니다.

---

## 주요 기능

- **사주 팔자 분석** — sajupy 라이브러리로 사주를 계산하고 Gemini AI가 투자 성향 중심의 풀이 생성
- **자유형식 포트폴리오 파싱** — 텍스트로 입력한 포트폴리오를 AI가 구조화된 데이터로 변환 (KRW/USD 자동 환산)
- **AI 리밸런싱 제안** — 사주 용신·기신과 사용자 선호 전략을 종합한 매수/매도/유지 액션 테이블 생성
- **결과 공유** — UUID 기반 고유 URL로 리밸런싱 결과 공유
- **사주 캐싱** — 동일한 생년월일/시진/성별 조합은 DB에서 즉시 반환 (Gemini 재호출 없음)

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | React 18, TypeScript, Vite |
| Backend | FastAPI, Python 3.12, uvicorn |
| AI | Google Gemini 2.5 Flash (`google-genai`) |
| 사주 계산 | sajupy |
| DB | SQLAlchemy + SQLite (MySQL 전환 가능) |
| 패키지 관리 | uv (backend), npm (frontend) |

---

## 시작하기

### 사전 요구사항

- Python 3.12+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (Python 패키지 매니저)
- Google Gemini API 키

### 1. 저장소 클론

```bash
git clone <repository-url>
cd saju-rebalancer
```

### 2. 백엔드 설정

```bash
cd backend
cp .env.example .env
# .env 파일에 GEMINI_API_KEY 입력
```

```bash
# 의존성 설치 및 서버 실행
uv run uvicorn main:app --reload
# → http://localhost:8000
```

### 3. 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

Vite 개발 서버는 `/api/*` 요청을 `localhost:8000`으로 자동 프록시합니다.

---

## 사용 방법

1. **Step 1 — 사주 입력**: 생년월일, 태어난 시(시진), 성별을 입력하고 분석 시작
2. **Step 2 — 포트폴리오 입력**: 보유 자산을 자유 형식으로 입력 (예: "삼성전자 100주 8만원, AAPL 10주 $190") → AI가 파싱 후 확인 → 운영 방안/선호 전략 입력
3. **Step 3 — 결과 확인**: 사주 기둥, AI 풀이, 리밸런싱 표(매수/매도/유지), 종합 해설 출력 → 고유 URL로 공유 가능

---

## 프로젝트 구조

```
saju-rebalancer/
├── backend/
│   ├── main.py                  # FastAPI 앱 진입점
│   ├── database.py              # SQLAlchemy 엔진/세션
│   ├── models.py                # SajuCache ORM 모델
│   ├── schemas.py               # Pydantic 요청/응답 스키마
│   ├── routers/
│   │   ├── saju.py              # POST /api/saju/analyze
│   │   ├── portfolio.py         # POST /api/portfolio/parse
│   │   ├── rebalance.py         # POST /api/rebalance/analyze
│   │   └── report.py            # GET  /api/report/{uuid}
│   └── services/
│       ├── gemini_service.py    # Gemini API 래퍼
│       ├── saju_service.py      # 사주 계산 + DB 캐시 로직
│       └── portfolio_service.py # 포트폴리오 파싱
└── frontend/
    └── src/
        ├── App.tsx              # 스텝 상태 관리, 라우팅
        ├── types.ts             # 백엔드 스키마와 대응하는 TS 타입
        ├── api/client.ts        # fetch 래퍼
        └── components/
            ├── Step1SajuInput.tsx
            ├── Step2PortfolioInput.tsx
            ├── Step3Results.tsx
            └── RebalancingReportPage.tsx
```

---

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/api/saju/analyze` | 사주 팔자 계산 + 풀이 (결과 캐싱) |
| POST | `/api/portfolio/parse` | 자유형식 텍스트 → 구조화된 포트폴리오 |
| POST | `/api/rebalance/analyze` | 통합 리밸런싱 분석 |
| GET  | `/api/report/{uuid}` | 저장된 리밸런싱 결과 조회 |
| GET  | `/health` | 헬스체크 |

---

## 환경변수

`backend/.env` 파일:

```env
GEMINI_API_KEY=your_gemini_api_key_here

# SQLite (기본값, 별도 설정 불필요)
# DATABASE_URL=sqlite:///./saju.db

# MySQL로 전환 시
# DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname
```

MySQL 전환 시 `uv add pymysql` 추가 필요.

---

## 개발 명령어

```bash
# 백엔드
cd backend
uv run uvicorn main:app --reload   # 개발 서버
uv add <package>                   # 패키지 추가
uv remove <package>                # 패키지 제거

# 프론트엔드
cd frontend
npm run dev      # 개발 서버
npm run build    # 프로덕션 빌드
npm run lint     # ESLint
```
