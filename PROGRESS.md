# PROGRESS.md

현재까지 완료된 작업을 기록한다.
작업 완료 시 날짜와 함께 업데이트한다.

---

## 현재 상태

**전체 기능 완료, 서비스 운영 중** (https://saju.daehyeoni.dev)
**다음**: 백로그 항목 중 우선순위에 따라 개선

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
| 2026-03-19 | Docker Compose 배포 설정 (GHCR 이미지, GitHub Actions 릴리즈) |
| 2026-03-19 | Docker Compose 포트 파라미터화 (`${FRONTEND_PORT:-80}`), `.env.example` 루트 생성 |
| 2026-03-19 | OS Nginx reverse proxy 설정 (saju.daehyeoni.dev 서브도메인) |
| 2026-03-19 | 사용자 Gemini API 키 입력 기능 (`ApiKeyModal`, sessionStorage, `X-Gemini-Api-Key` 헤더) |
| 2026-03-19 | 백엔드 전체 라우터/서비스에 `api_key` 파라미터 전파 |
| 2026-03-19 | IntroPage 무료 티어 안내 배너 + 자체 호스팅 GitHub 링크 |
| 2026-03-19 | UI 버그 수정: 모달 투명, 버튼 겹침, CompatibilityPage API 키 버튼 누락 |
| 2026-03-19 | 한국 주식 검색 플레이스홀더/힌트 수정 (한국어만 지원 명시) |
| 2026-03-19 | README 스크린샷 프리뷰 추가 (`docs/images/` — intro, rebalancer, compatibility) |
| 2026-03-19 | 궁합 점수 단기/중기/장기 분리 (`TermScore`, 3-card grid, i18n 추가) |
| 2026-03-19 | CLAUDE.md 세션 시작 시 PLAN.md·PROGRESS.md 읽기 지침 추가 |
| 2026-03-19 | PLAN.md·PROGRESS.md 현재 상태로 동기화 |

---

## 다음 할 일 (백로그)

- 리밸런싱 스트리밍 응답 안정성 개선
- 모바일 반응형 세부 개선
- CEO 검색 품질 모니터링 및 개선
- 에러 상태 UX 개선 (재시도, 상세 오류 메시지)
- 다크모드 지원
