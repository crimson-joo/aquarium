# Graph Report - aquarium  (2026-06-30)

## Corpus Check
- 90 files · ~19,035 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 629 nodes · 730 edges · 85 communities (84 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `52c37fff`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]

## God Nodes (most connected - your core abstractions)
1. `run_aquarium_pipeline()` - 30 edges
2. `LifecycleStore` - 25 edges
3. `Aquarium / 아쿠아리움` - 19 edges
4. `Aquarium Architecture Slice` - 15 edges
5. `Aquarium Architecture Slice` - 15 edges
6. `_native_simulation()` - 11 edges
7. `아쿠아리움 Design Slice` - 11 edges
8. `create_app()` - 10 edges
9. `JobWorker` - 10 edges
10. `Release — Aquarium` - 10 edges

## Surprising Connections (you probably didn't know these)
- `create_app()` --calls--> `LifecycleStore`  [INFERRED]
  backend/app/main.py → backend/app/domain/lifecycle.py
- `create_app()` --calls--> `JobWorker`  [INFERRED]
  backend/app/main.py → backend/app/domain/lifecycle.py
- `test_rejects_unsupported_locale()` --calls--> `create_app()`  [INFERRED]
  backend/tests/test_api.py → backend/app/main.py
- `test_retry_rejects_non_terminal_job()` --calls--> `create_app()`  [INFERRED]
  backend/tests/test_api.py → backend/app/main.py
- `test_startup_marks_interrupted_running_jobs_failed()` --calls--> `create_app()`  [INFERRED]
  backend/tests/test_api.py → backend/app/main.py

## Communities (85 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (50): BaseModel, msg(), AdapterStage, HandoffManifest, Ontology, OntologyEntity, Persona, PipelineResult (+42 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (47): 목표, 1. 목표와 비목표, 10. Tests 전략, 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처 (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (8): ChatRequest, CreateRunRequest, Locale, SimulationMode, JobWorker, LifecycleStore, _now(), StrEnum

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (30): 1. 제품/브랜드 방향, 10. 구현팀 전달 메모, 2.1 권장 전역 구조, 2.2 신규 사용자용 5단계 플로우, 2. 정보 구조 및 핵심 UX 플로우, 3. 주요 화면 제안, 3.1 Home / Landing, 3.2 New Aquarium / Seed Intake (+22 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (27): 빠른 시작, 프로젝트 문서, 중요한 한계, 프로젝트 문서, 중요한 한계, 실제 adapter 연결, Aquarium / 아쿠아리움, code:bash (cp .env.example .env) (+19 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (26): 목표, 다음 작업 추천, 다음 작업 추천, 다음 작업 추천, 실행 단계, 다음 작업 추천, 실행 단계, 현재 완료 상태 (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (24): 현재 상태, 빠른 시작, 빠른 시작, 프로젝트 문서, 중요한 한계, 프로젝트 문서, 프로젝트 문서, 프로젝트 문서 (+16 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (16): messages, Entity, GraphMemoryKey, JobResult, JobStatus, Locale, Mode, Persona (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (15): create_app(), _data_dir(), _load_run_payload(), _result_path(), _run_response(), BaseSettings, get_settings(), Settings (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (13): 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처, 5. Frontend 구조, 8. i18n 전략, Aquarium Architecture Slice (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (13): 현재 기본 실행 경로, code:text (docker compose up --build), code:bash (AQUARIUM_BETTAFISH_COMMAND="python3 /Users/crimson/Projects/), code:bash (cd backend && uv run pytest -q), Docker endpoints, GitHub Actions contract, Legacy sibling-runner 통합 실행 경로, Local release gate (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (9): 1. 환경 파일 준비, 2. Docker Compose 실행, 3. 접속, 4. 로컬 개발 검증, 5. 현재 MVP 주의사항, Aquarium Quickstart, code:bash (cp .env.example .env), code:bash (docker compose up --build) (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (9): 2026-06-29 — Initial MVP scaffold, 2026-06-29 — Real runner canary and state visibility, 2026-06-29 — Real runner release, 2026-06-30 — Native MiroFish runtime canary, 2026-06-30 — Native Productization Pass 1, 2026-06-30 — Production Readiness Pass 1, 2026-06-30 — Runtime evidence labeling and multiverse expansion, 2026-06-30 — Standalone Aquarium native pivot (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (9): 7. Job flow와 handoff contract, code:text (POST /api/runs), code:json ({), Stage 1: ResearchReport, Stage 2: SeedDocument, Stage 3: Ontology/Persona extraction, Stage 4: Simulation, Stage 5: SimulationReport (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (7): 현재 검증 상태, Acceptance criteria, Docker, Fail-closed, i18n, Product flow, QA — Aquarium

### Community 15 - "Community 15"
Cohesion: 0.54
Nodes (7): _allowed_extra_env_names(), _command_env(), _read_json(), run_bettafish_cli_adapter(), _run_command(), run_mirofish_cli_adapter(), _validate_simulation_report_artifact()

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (7): 한 줄 정의, 성공 순간, 성공 순간, MVP 목표, Non-goals, Product — Aquarium, Product positioning

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (7): 10. Tests 전략, CI 최소 세트, code:text (lint backend), Contract tests, E2E/UI tests, Integration tests, Unit tests

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (6): 9. Provider/env 설계, code:env (APP_ENV=local), `.env.example`, Native engine package boundary, Production Readiness Pass 1 lifecycle, Provider profiles

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 29 - "Community 29"
Cohesion: 0.4
Nodes (4): code:json ({), Handoff Manifest v1, Policy, Schema

### Community 30 - "Community 30"
Cohesion: 0.6
Nodes (3): test_real_integration_canary_fails_when_runner_provider_is_not_real(), test_real_integration_canary_passes_with_fake_contract_runners(), _write_executable()

### Community 31 - "Community 31"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 32 - "Community 32"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (4): 6. Storage 모델, code:text (data/), File storage, PostgreSQL 테이블

### Community 34 - "Community 34"
Cohesion: 0.5
Nodes (4): 3. Docker Compose 서비스, code:bash (cp .env.example .env), optional profile, 기본 profile

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 38 - "Community 38"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 39 - "Community 39"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (3): 핵심 신호, 핸드오프 메모, 조사 보고서: AI 검색엔진 시장 변화

### Community 41 - "Community 41"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아직 대기, 핵심 신호, 핸드오프 메모

### Community 42 - "Community 42"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 44 - "Community 44"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 45 - "Community 45"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 48 - "Community 48"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 49 - "Community 49"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 50 - "Community 50"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아쿠아리움 도커 스모크, 핵심 신호, 핸드오프 메모

### Community 51 - "Community 51"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 52 - "Community 52"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아직 대기, 핵심 신호, 핸드오프 메모

### Community 53 - "Community 53"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 54 - "Community 54"
Cohesion: 0.5
Nodes (3): Aquarium Docs, Canonical current docs, Setup docs

### Community 55 - "Community 55"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 56 - "Community 56"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 57 - "Community 57"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 58 - "Community 58"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 59 - "Community 59"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 60 - "Community 60"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 61 - "Community 61"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 62 - "Community 62"
Cohesion: 0.5
Nodes (3): 조사 보고서: 취소 후 재개, 핵심 신호, 핸드오프 메모

### Community 63 - "Community 63"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아직 대기, 핵심 신호, 핸드오프 메모

### Community 64 - "Community 64"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 65 - "Community 65"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 66 - "Community 66"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 67 - "Community 67"
Cohesion: 0.5
Nodes (3): 조사 보고서: 로컬 검색엔진 기반 보고서, 핵심 신호, 핸드오프 메모

### Community 68 - "Community 68"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 69 - "Community 69"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아직 대기, 핵심 신호, 핸드오프 메모

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (3): 4. Backend 구조, API 최소 세트, code:text (backend/)

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (3): 목표, 1. 목표와 비목표, 비목표

## Knowledge Gaps
- **267 isolated node(s):** `consoleErrors`, `Locale`, `Mode`, `Stage`, `ProviderKey` (+262 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LifecycleStore` connect `Community 2` to `Community 8`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `run_aquarium_pipeline()` connect `Community 0` to `Community 15`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `create_app()` connect `Community 8` to `Community 2`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `run_aquarium_pipeline()` (e.g. with `RunRecord` and `run_bettafish_cli_adapter()`) actually correct?**
  _`run_aquarium_pipeline()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `LifecycleStore` (e.g. with `CreateRunRequest` and `ChatRequest`) actually correct?**
  _`LifecycleStore` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `consoleErrors`, `Locale`, `Mode` to the rest of the system?**
  _267 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._