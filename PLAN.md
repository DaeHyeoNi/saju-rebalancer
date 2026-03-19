# PLAN.md — 사주 리밸런서

최종 업데이트: 2026-03-19

---

## 현재 상태

**모든 주요 기능 완료** — 서비스 운영 중 (https://saju.daehyeoni.dev)

---

## 완료된 Phase

### Phase 1: 프로젝트 기반
- [x] FastAPI 백엔드 기본 구조 (routers, services, models)
- [x] React + Vite 프론트엔드 3단계 위저드
- [x] Gemini API 연동 (사주풀이, 포트폴리오 파싱, 리밸런싱)
- [x] SQLite 사주 캐시
- [x] UUID 기반 리밸런싱 리포트 공유
- [x] PLAN.md, PROGRESS.md 작성

### Phase 2: 백엔드 리팩토링
- [x] `CeoCache`, `CeoFeedback` DB 모델 추가
- [x] `services/ceo_search_service.py` — DuckDuckGo + Gemini CEO 조회
- [x] `services/gemini_service.py` — `generate_saju_compatibility()` 추가
- [x] `routers/compatibility.py` — /lookup, /analyze, /report 엔드포인트

### Phase 3: 주식 사주 궁합 기능
- [x] 프론트 라우팅 재편 (`/` 인트로 → `/rebalancer`, `/compatibility`)
- [x] `IntroPage.tsx` — 히어로 기능 선택 화면
- [x] `CompatibilityPage.tsx` — CEO 검색/수동입력/시진/신고/결과 전체 플로우
- [x] 궁합 점수 단기/중기/장기로 분리 (`TermScore`, 3-card grid)

### Phase 4: 배포 및 인프라
- [x] Docker Compose 배포 설정 (GHCR 이미지, GitHub Actions 릴리즈)
- [x] Docker Compose 포트 파라미터화 (`${FRONTEND_PORT:-80}`)
- [x] `.env.example` 루트 파일 생성
- [x] OS Nginx reverse proxy 설정 (subdomain: saju.daehyeoni.dev)
- [x] Cloudflare DNS + SSL 설정

### Phase 5: 사용자 Gemini API 키 기능
- [x] `ApiKeyModal.tsx` — sessionStorage 기반 API 키 입력/저장/삭제
- [x] `api/client.ts` — `X-Gemini-Api-Key` 헤더 자동 주입
- [x] 모든 백엔드 라우터에 `x_gemini_api_key` 헤더 파라미터 추가
- [x] 모든 Gemini 서비스 메서드에 `api_key` 파라미터 추가
- [x] IntroPage 무료 티어 안내 배너 + 자체 호스팅 GitHub 링크
- [x] WizardApp / CompatibilityPage 헤더에 API 키 버튼 추가
- [x] i18n (ko/en) `apiKey.*` 키 추가

### Phase 6: UI 버그 수정 및 개선
- [x] 모달 투명 버그 수정 (`var(--color-surface)` → `var(--color-bg-card, #fffcf8)`)
- [x] 헤더 API 키 버튼 ↔ 언어 전환 버튼 겹침 수정
- [x] CompatibilityPage API 키 버튼 추가 (누락)
- [x] 한국 주식 검색 영문 플레이스홀더 → 한국어만 지원 안내로 수정
- [x] README 스크린샷 프리뷰 추가 (docs/images/)

---

## 향후 개선 사항 (백로그)

- [ ] 리밸런싱 스트리밍 응답 안정성 개선
- [ ] 모바일 반응형 세부 개선
- [ ] CEO 검색 품질 모니터링 및 개선
- [ ] 에러 상태 UX 개선 (재시도, 상세 오류 메시지)
- [ ] 다크모드 지원
