# Graph Report - aquarium  (2026-06-30)

## Corpus Check
- 45 files · ~13,691 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 399 nodes · 494 edges · 36 communities
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 54 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e261f265`
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

## God Nodes (most connected - your core abstractions)
1. `run_aquarium_pipeline()` - 30 edges
2. `Aquarium / 아쿠아리움` - 16 edges
3. `Aquarium Architecture Slice` - 15 edges
4. `Aquarium Architecture Slice` - 15 edges
5. `_native_simulation()` - 11 edges
6. `아쿠아리움 Design Slice` - 11 edges
7. `Release — Aquarium` - 10 edges
8. `실행 단계` - 9 edges
9. `3. 주요 화면 제안` - 9 edges
10. `Aquarium 실행계획 — stub MVP에서 실제 BettaFish→MiroFish 통합 제품까지` - 9 edges

## Surprising Connections (you probably didn't know these)
- `_native_simulation()` --calls--> `build_personas()`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/engines/persona/native.py
- `run_aquarium_pipeline()` --calls--> `run_bettafish_cli_adapter()`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/adapters.py
- `run_aquarium_pipeline()` --calls--> `run_mirofish_cli_adapter()`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/adapters.py
- `test_pipeline_uses_configured_bettafish_cli_adapter()` --calls--> `run_aquarium_pipeline()`  [INFERRED]
  backend/tests/test_external_adapters.py → backend/app/domain/pipeline.py
- `test_pipeline_rejects_mismatched_bettafish_provider()` --calls--> `run_aquarium_pipeline()`  [INFERRED]
  backend/tests/test_external_adapters.py → backend/app/domain/pipeline.py

## Communities (36 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (47): ChatRequest, CreateRunRequest, BaseModel, msg(), AdapterStage, HandoffManifest, Locale, Ontology (+39 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (39): 목표, 1. 목표와 비목표, 10. Tests 전략, 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처 (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (38): 목표, 1. 목표와 비목표, 10. Tests 전략, 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처 (+30 more)

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
Cohesion: 0.12
Nodes (21): 현재 상태, 빠른 시작, 프로젝트 문서, 중요한 한계, 프로젝트 문서, 프로젝트 문서, 프로젝트 문서, 중요한 한계 (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (14): messages, Entity, GraphMemoryKey, Locale, Mode, Persona, ProviderKey, ResultTab (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (13): 현재 기본 실행 경로, code:text (docker compose up --build), code:bash (AQUARIUM_BETTAFISH_COMMAND="python3 /Users/crimson/Projects/), code:bash (cd backend && uv run pytest -q), Docker endpoints, GitHub Actions contract, Legacy sibling-runner 통합 실행 경로, Local release gate (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.23
Nodes (9): create_app(), _data_dir(), _result_path(), _run_response(), BaseSettings, get_settings(), Settings, test_create_run_and_chat() (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.2
Nodes (9): 1. 환경 파일 준비, 2. Docker Compose 실행, 3. 접속, 4. 로컬 개발 검증, 5. 현재 MVP 주의사항, Aquarium Quickstart, code:bash (cp .env.example .env), code:bash (docker compose up --build) (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (8): 2026-06-29 — Initial MVP scaffold, 2026-06-29 — Real runner canary and state visibility, 2026-06-29 — Real runner release, 2026-06-30 — Native MiroFish runtime canary, 2026-06-30 — Native Productization Pass 1, 2026-06-30 — Runtime evidence labeling and multiverse expansion, 2026-06-30 — Standalone Aquarium native pivot, Changelog — Aquarium

### Community 12 - "Community 12"
Cohesion: 0.42
Nodes (8): test_adapter_env_does_not_leak_unallowlisted_secret(), test_pipeline_rejects_mirofish_completed_result_with_body_that_does_not_match_report_file(), test_pipeline_rejects_mirofish_completed_result_with_missing_report_path(), test_pipeline_rejects_mirofish_report_path_outside_run_dir(), test_pipeline_rejects_mismatched_bettafish_provider(), test_pipeline_uses_configured_bettafish_cli_adapter(), test_pipeline_uses_configured_mirofish_cli_adapter(), _write_executable()

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (9): 7. Job flow와 handoff contract, code:text (POST /api/runs), code:json ({), Stage 1: ResearchReport, Stage 2: SeedDocument, Stage 3: Ontology/Persona extraction, Stage 4: Simulation, Stage 5: SimulationReport (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (9): 7. Job flow와 handoff contract, code:text (POST /api/runs), code:json ({), Stage 1: ResearchReport, Stage 2: SeedDocument, Stage 3: Ontology/Persona extraction, Stage 4: Simulation, Stage 5: SimulationReport (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.25
Nodes (7): 한 줄 정의, 성공 순간, 성공 순간, MVP 목표, Non-goals, Product — Aquarium, Product positioning

### Community 16 - "Community 16"
Cohesion: 0.54
Nodes (7): _allowed_extra_env_names(), _command_env(), _read_json(), run_bettafish_cli_adapter(), _run_command(), run_mirofish_cli_adapter(), _validate_simulation_report_artifact()

### Community 17 - "Community 17"
Cohesion: 0.25
Nodes (7): 현재 검증 상태, Acceptance criteria, Docker, Fail-closed, i18n, Product flow, QA — Aquarium

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (4): code:json ({), Handoff Manifest v1, Policy, Schema

### Community 20 - "Community 20"
Cohesion: 0.6
Nodes (3): test_real_integration_canary_fails_when_runner_provider_is_not_real(), test_real_integration_canary_passes_with_fake_contract_runners(), _write_executable()

### Community 21 - "Community 21"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 22 - "Community 22"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아쿠아리움 도커 스모크, 핵심 신호, 핸드오프 메모

### Community 23 - "Community 23"
Cohesion: 0.5
Nodes (3): Aquarium Docs, Canonical current docs, Setup docs

### Community 24 - "Community 24"
Cohesion: 0.5
Nodes (3): 핵심 신호, 핸드오프 메모, 조사 보고서: AI 검색엔진 시장 변화

## Knowledge Gaps
- **179 isolated node(s):** `Locale`, `Mode`, `Stage`, `ProviderKey`, `StatusKey` (+174 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_aquarium_pipeline()` connect `Community 0` to `Community 16`, `Community 12`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `Aquarium Architecture Slice` connect `Community 1` to `Community 14`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Aquarium Architecture Slice` connect `Community 2` to `Community 13`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `run_aquarium_pipeline()` (e.g. with `RunRecord` and `run_bettafish_cli_adapter()`) actually correct?**
  _`run_aquarium_pipeline()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Locale`, `Mode`, `Stage` to the rest of the system?**
  _179 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._