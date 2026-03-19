# PROGRESS.md

현재까지 완료된 작업을 기록한다.
작업 완료 시 날짜와 함께 업데이트한다.

---

## 현재 상태

**Phase 1~4 완료** — 주식 사주 궁합 기능 추가 + 프론트엔드 리팩토링
**다음**: 실 서버 테스트 및 디자인 피드백 반영

---

## 완료된 작업

| 날짜 | 내용 |
|------|------|
| 2026-03-19 이전 | FastAPI 백엔드 기본 구조 (routers, services, models) |
| 2026-03-19 이전 | React + Vite 프론트엔드 3단계 위저드 |
| 2026-03-19 이전 | Gemini API 연동 (사주풀이, 포트폴리오 파싱, 리밸런싱) |
| 2026-03-19 이전 | SQLite 사주 캐시 (KST 기준) |
| 2026-03-19 이전 | UUID 기반 리밸런싱 리포트 공유 기능 |
| 2026-03-19 | PLAN.md, PROGRESS.md 작성 |
| 2026-03-19 | Phase 1: `.claude/skills/saju-domain/`, `.claude/commands/` 추가 |
| 2026-03-19 | Phase 2: `CeoCache`, `CeoFeedback` DB 모델 추가 |
| 2026-03-19 | Phase 2: `services/ceo_search_service.py` — DuckDuckGo + Gemini CEO 조회 |
| 2026-03-19 | Phase 2: `services/gemini_service.py` — `generate_saju_compatibility()` 추가 |
| 2026-03-19 | Phase 2: `routers/compatibility.py` — /lookup, /analyze, /report 엔드포인트 |
| 2026-03-19 | Phase 3: 프론트 라우팅 재편 (`/` 인트로 → `/rebalancer`, `/compatibility`) |
| 2026-03-19 | Phase 3: `IntroPage.tsx` — 히어로 기능 선택 화면 |
| 2026-03-19 | Phase 4: `CompatibilityPage.tsx` — CEO 검색/수동입력/시진/신고/결과 전체 플로우 |
| 2026-03-19 | Phase 4: `App.css` — 인트로·궁합 전용 스타일 + 반응형 추가 |

---

## 다음 할 일

- 실 서버 테스트 (DuckDuckGo CEO 검색 품질 확인)
- 디자인 피드백 반영
