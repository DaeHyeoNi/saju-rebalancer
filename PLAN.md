# PLAN.md — 사주 리밸런서 v2

작성일: 2026-03-19
목표: 전체 리팩토링 + 디자인 개선 + 주식 사주 궁합 기능 추가

---

## 현재 상태

- FastAPI 백엔드 + React/Vite 프론트엔드 동작 중
- 3단계 위저드: 사주 입력 → 포트폴리오 입력 → 리밸런싱 결과
- UUID 기반 리포트 공유 기능 있음
- Gemini API (gemini-3.1-flash-lite-preview) 사용

---

## Phase 1: 프로젝트 관리 구조 세팅

- [x] `PLAN.md` 작성 (현재 파일)
- [ ] `PROGRESS.md` 작성
- [ ] `.claude/skills/saju-domain/SKILL.md` — 사주 리밸런서 도메인 지식
- [ ] `.claude/commands/` — 유용한 슬래시 커맨드 추가
  - `dev.md` — 개발 서버 실행
  - `reset-db.md` — DB 초기화

---

## Phase 2: 백엔드 리팩토링

### 2-1. `gemini_service.py` 정리
- [ ] `generate_saju_compatibility()` 메서드 추가 (궁합 분석)
- [ ] `search_ceo_birthdate()` — Gemini Google Search grounding으로 CEO 생년월일 검색

### 2-2. 새 서비스 파일
- [ ] `services/ceo_search_service.py` — 주식 티커 → CEO 이름 + 생년월일 조회
  - `duckduckgo-search` 패키지로 검색 후 Gemini로 파싱 (무료, API 키 불필요)
  - 결과 캐싱 (SQLite, `CeoCache` 테이블)

### 2-3. 새 라우터
- [ ] `routers/compatibility.py` — `/api/compatibility/analyze`

### 2-4. 스키마 추가
- [ ] `schemas.py`에 `CompatibilityRequest`, `CompatibilityResponse` 추가

### 2-5. DB 모델
- [ ] `models.py`에 `CeoCache` 테이블 추가
  - 키: `ticker`
  - 값: `ceo_name`, `ceo_birth_date`, `company_name`

---

## Phase 3: 주식 사주 궁합 기능 (신규)

### 기능 흐름

```
사용자 입력: 생년월일 + 주식 티커 (예: TSLA)
      ↓
[Gemini + Google Search] 티커 → CEO 이름 + 생년월일 조회
      ↓
[sajupy] 사용자 사주 계산 + CEO 사주 계산
      ↓
[Gemini] 두 사주 궁합 분석 → 투자 적합도 + 해설
```

### 궁합 분석 내용
- 사용자 일간(日干) vs CEO 일간 오행 관계
- 사주 음양 균형 및 상생/상극 관계
- 재성(財星) 흐름 — 이 주식이 나에게 재물을 가져다주는가
- 종합 투자 적합도 (★ 1~5)
- 매수/관망/주의 권고

### API 엔드포인트

```
POST /api/compatibility/analyze
{
  "birth_date": "1990-01-15",
  "birth_hour": "자시",
  "gender": "남",
  "ticker": "TSLA"
}

→ {
  "ceo_name": "일론 머스크",
  "ceo_birth_date": "1971-06-28",
  "company_name": "Tesla",
  "user_pillars": {...},
  "ceo_pillars": {...},
  "compatibility_score": 4,
  "compatibility_reading": "...",
  "recommendation": "매수"
}
```

---

## Phase 4: 프론트엔드 리팩토링 + 디자인 개선

### 4-1. 라우팅 구조 변경

```
/              → 홈 (기능 선택)
/rebalancer    → 기존 사주 리밸런서 (3단계 위저드)
/compatibility → 주식 사주 궁합
/report/:uuid  → 리밸런싱 리포트 공유
```

### 4-2. 디자인 시스템

- **컬러**: 기존 골드/딥퍼플 톤 유지 + 개선
- **타이포**: 한글 가독성 중심
- **반응형**: 모바일 우선 (375px ~ 1440px)
- **분위기**: 신비롭고 고급스러운 운세 앱 느낌
- **컴포넌트**: 공통 Card, Button, Badge, LoadingSpinner 추출

### 4-3. 새 컴포넌트

- [ ] `components/common/` — 공통 UI 컴포넌트
- [ ] `pages/HomePage.tsx` — 기능 선택 랜딩
- [ ] `pages/RebalancerPage.tsx` — 기존 리밸런서 위저드
- [ ] `pages/CompatibilityPage.tsx` — 주식 사주 궁합
- [ ] `components/CompatibilityResult.tsx` — 궁합 결과 카드

---

## 작업 순서

1. Phase 1 — 프로젝트 관리 파일 (즉시)
2. Phase 2 — 백엔드 리팩토링 + 새 기능
3. Phase 3 — 궁합 기능 프론트엔드
4. Phase 4 — 전체 디자인 개선

---

## 기술 결정 사항

| 항목 | 결정 | 이유 |
|------|------|------|
| CEO 검색 방법 | DuckDuckGo Search (`duckduckgo-search` 패키지) + Gemini 파싱 | 무료, API 키 불필요 |
| 사주 계산 | 기존 `sajupy` 재사용 | 이미 검증됨 |
| 궁합 LLM | gemini-3.1-flash-lite-preview | 기존 모델 유지 |
| CEO 캐시 | SQLite `CeoCache` 테이블 | 반복 검색 방지 |
| 프론트 라우팅 | React Router (기존 유지) | 추가 의존성 없음 |
