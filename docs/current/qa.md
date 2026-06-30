# QA — Aquarium

## 현재 검증 상태

MVP vertical slice 기준 검증 완료:

- Backend contract/pipeline tests: 통과
- Backend API tests: 통과
- Frontend i18n test: 통과
- Frontend production build: 통과

Standalone native 기준:

- 기본 runner 미설정 상태는 `aquarium_native` provider로 완료되어야 한다.
- API/UI `runtime_claim.runtime_level`은 `aquarium_native`, `standalone_native=true`, `external_runner_dependency=false`를 표시해야 한다.
- API/UI는 `graph_engine_status=aquarium_native`와 `graph_memory_status=not_configured`를 분리해 표시해야 한다. Aquarium 자체 생태계 지도 PASS를 Graphiti memory PASS로 오해시키면 안 된다.
- 외부 BettaFish/MiroFish repo 호출 없이 topic → seed → ontology/persona → simulation → report/chat이 완료되어야 한다.
- API response와 UI는 seed key points, ecosystem entities/relations, personas, universe events, report preview를 탐색 가능한 결과 패널로 제공해야 한다.

Legacy runner 통합 canary 기준:

- `scripts/run_real_integration_canary.sh`가 추가되었다.
- runner 미설정 상태는 standalone 제품 경로로는 정상(`aquarium_native`)이지만, sibling-runner real integration canary에서는 `real_integration=false`와 exit code `2`를 반환해야 한다.
- real PASS 조건은 BettaFish=`bettafish_cli completed`, MiroFish=`mirofish_cli completed` 둘 다 만족할 때뿐이다.
- 2026-06-30 추가 검증에서 fake bridge 없이 live MiroFish backend + Graphiti + OASIS bounded single run까지 통과했다.

Release QA 결과:

- BettaFish Aquarium runner tests: 11 passed.
- MiroFish Aquarium runner tests: 11 passed.
- Aquarium backend tests: 14 passed.
- Aquarium frontend i18n tests: 2 passed.
- Frontend production build: passed.
- Docker Compose config/build/up health smoke: passed.
- Browser smoke: Korean UI rendered, run completed, warnings/artifacts visible, console errors 0.
- GitHub Actions: Aquarium main `Local Runtime CI` success; MiroFish-localized main `Local Runtime CI` and `Deploy GitHub Pages` success.
- Native runtime canary: `pass`, `real_integration=true`, run `aq_25badceb79ca`.
  - BettaFish provider: `bettafish_cli`, completed.
  - MiroFish provider: `mirofish_cli`, completed.
  - MiroFish graph: `local_mirofish_3660f13154484f5b`, 10 nodes / 38 edges.
  - Simulation: `sim_3c7675d86e46`, graph memory update enabled, 16 meaningful actions.
  - Report: `report_d385e3807800`, Korean report generated with CJK leakage 0.
- API/UI runtime labeling: `runtime_claim` exposes standalone native / external runner dependency / real-degraded-native boundary; focused backend tests 14 passed and frontend build passed after the change.
- Productization pass 1: native engines split into `research`, `graph`, `persona`, `simulation`, `report` packages; API returns explorable `seed`/`ecosystem`/`simulation`/`report`; UI tabs show 조사 Seed/생태계 지도/해류 관찰/리포트; browser smoke showed Graphiti memory as not configured rather than PASS; console errors 0.
- Production Readiness Pass 1: `POST /api/runs` now creates a DB-backed job and returns `202`; lifecycle polling, cancel, retry, resume, progress/stage, attempts, and result persistence are covered by backend tests. UI shows job progress/failure controls, and Playwright E2E covers job creation through result tabs with console errors 0.
- MiroFish live-local multiverse canary: `PASS`, `mv_4ef846551b2d`, 4 universes / 24 configured rounds / graph memory preflight healthy / ensemble comparison produced 3 clusters and 4 sensitivity axes.

중요 caveat: Aquarium native canary는 live native Graphiti/OASIS 경로를 통과한 bounded single-run smoke다. MiroFish multiverse 확장은 live endpoint preflight + bounded real-backend comparison PASS로 확인했지만, durable OASIS action stream이 쌓이는 장시간 production run으로 격상하려면 별도 장시간 실행이 필요하다.

## Acceptance criteria

### Product flow

- 주제 입력 → Aquarium native research seed → handoff manifest → ontology/persona → simulation → report 순서가 한 run 안에서 완료되어야 한다.
- single mode는 하나의 universe를 생성해야 한다.
- multiverse mode는 3개 universe와 ensemble frequency caveat를 생성해야 한다.

### i18n

- UI copy는 한국어/중국어/영어를 모두 제공해야 한다.
- 보고서와 chat answer는 locale metadata를 따라야 한다.
- 중국어는 지원 언어 중 하나일 뿐 기본 source/tone처럼 보이면 안 된다.

### Fail-closed

- unsupported locale은 API validation error를 반환해야 한다.
- handoff manifest/report path는 명시적으로 저장되어야 한다.
- `aquarium_native`는 standalone 실행으로 표시되어야 하며, `local_stub`/legacy fallback을 native 성공으로 오인시키면 안 된다.

### Docker

- `docker compose config --quiet`가 통과해야 한다.
- `docker compose up --build` 후 UI/API가 응답해야 한다.
- Playwright E2E는 Docker Compose runtime에서 job lifecycle → result tabs → Graphiti memory caveat를 검증해야 한다.
