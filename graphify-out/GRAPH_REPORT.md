# Graph Report - feat-adapter-orchestration  (2026-06-29)

## Corpus Check
- 29 files · ~8,910 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 303 nodes · 348 edges · 30 communities (29 shown, 1 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f18cce6`
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
1. `run_aquarium_pipeline()` - 21 edges
2. `Aquarium Architecture Slice` - 15 edges
3. `Aquarium Architecture Slice` - 15 edges
4. `아쿠아리움 Design Slice` - 11 edges
5. `Aquarium / 아쿠아리움` - 9 edges
6. `3. 주요 화면 제안` - 9 edges
7. `7. Job flow와 handoff contract` - 8 edges
8. `7. Job flow와 handoff contract` - 8 edges
9. `_stub_simulation()` - 7 edges
10. `build_simulation_report()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `seed_from_report()` --calls--> `SeedDocument`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/contracts.py
- `extract_ontology()` --calls--> `OntologyEntity`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/contracts.py
- `extract_ontology()` --calls--> `Ontology`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/contracts.py
- `build_personas()` --calls--> `Persona`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/contracts.py
- `run_simulation()` --calls--> `UniverseResult`  [INFERRED]
  backend/app/domain/pipeline.py → backend/app/domain/contracts.py

## Communities (30 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (31): 목표, 1. 목표와 비목표, 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처, 비목표 (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (31): 목표, 1. 목표와 비목표, 11. Docs 구조, 12. 추천 초기 파일 구조, 13. Vertical slice 구현 순서, 14. 핵심 결정, 2. 최소 견고 아키텍처, 비목표 (+23 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (30): 1. 제품/브랜드 방향, 10. 구현팀 전달 메모, 2.1 권장 전역 구조, 2.2 신규 사용자용 5단계 플로우, 2. 정보 구조 및 핵심 UX 플로우, 3. 주요 화면 제안, 3.1 Home / Landing, 3.2 New Aquarium / Seed Intake (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (19): msg(), build_personas(), build_research_report(), build_simulation_report(), extract_ontology(), _key_points(), run_aquarium_pipeline(), _run_dir() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (22): 빠른 시작, 프로젝트 문서, 중요한 한계, Aquarium / 아쿠아리움, code:bash (cp .env.example .env), code:bash (cd backend), code:text (주제 입력), 현재 MVP 상태 (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (19): 목표, 다음 작업 추천, 실행 단계, 현재 완료 상태, Adapter command contract, Aquarium 실행계획 — stub MVP에서 실제 BettaFish→MiroFish 통합 제품까지, BettaFish command, code:text (AQUARIUM_TOPIC) (+11 more)

### Community 6 - "Community 6"
Cohesion: 0.22
Nodes (16): ChatRequest, CreateRunRequest, BaseModel, HandoffManifest, Locale, Ontology, OntologyEntity, Persona (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.24
Nodes (8): create_app(), _data_dir(), _result_path(), BaseSettings, get_settings(), Settings, test_create_run_and_chat(), test_rejects_unsupported_locale()

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (9): 1. 환경 파일 준비, 2. Docker Compose 실행, 3. 접속, 4. 로컬 개발 검증, 5. 현재 MVP 주의사항, Aquarium Quickstart, code:bash (cp .env.example .env), code:bash (docker compose up --build) (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (9): 7. Job flow와 handoff contract, code:text (POST /api/runs), code:json ({), Stage 1: ResearchReport, Stage 2: SeedDocument, Stage 3: Ontology/Persona extraction, Stage 4: Simulation, Stage 5: SimulationReport (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.28
Nodes (5): messages, Locale, Mode, RunResult, Stage

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (9): 7. Job flow와 handoff contract, code:text (POST /api/runs), code:json ({), Stage 1: ResearchReport, Stage 2: SeedDocument, Stage 3: Ontology/Persona extraction, Stage 4: Simulation, Stage 5: SimulationReport (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (7): 현재 검증 상태, Acceptance criteria, Docker, Fail-closed, i18n, Product flow, QA — Aquarium

### Community 13 - "Community 13"
Cohesion: 0.62
Nodes (6): _command_env(), _read_json(), run_bettafish_cli_adapter(), _run_command(), run_mirofish_cli_adapter(), AdapterStage

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (6): code:bash (cd backend && uv run pytest -q), Docker endpoints, Local release gate, 현재 release 수준, Release — Aquarium, Release caveat

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (7): 10. Tests 전략, CI 최소 세트, code:text (lint backend), Contract tests, E2E/UI tests, Integration tests, Unit tests

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (7): 10. Tests 전략, CI 최소 세트, code:text (lint backend), Contract tests, E2E/UI tests, Integration tests, Unit tests

### Community 17 - "Community 17"
Cohesion: 0.33
Nodes (5): 시뮬레이션 보고서, 앙상블 빈도, Universe 1, Universe 2, Universe 3

### Community 18 - "Community 18"
Cohesion: 0.33
Nodes (5): 한 줄 정의, 성공 순간, MVP 목표, Non-goals, Product — Aquarium

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (4): code:json ({), Handoff Manifest v1, Policy, Schema

### Community 20 - "Community 20"
Cohesion: 0.5
Nodes (3): Aquarium Docs, Canonical current docs, Setup docs

### Community 21 - "Community 21"
Cohesion: 0.5
Nodes (3): 시뮬레이션 보고서, 단일 해류, Single Current

### Community 22 - "Community 22"
Cohesion: 0.5
Nodes (3): 조사 보고서: 아쿠아리움 도커 스모크, 핵심 신호, 핸드오프 메모

### Community 23 - "Community 23"
Cohesion: 0.5
Nodes (3): 핵심 신호, 핸드오프 메모, 조사 보고서: AI 검색엔진 시장 변화

## Knowledge Gaps
- **145 isolated node(s):** `Locale`, `Mode`, `Stage`, `RunResult`, `현재 MVP 상태` (+140 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Aquarium Architecture Slice` connect `Community 1` to `Community 9`, `Community 15`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `Aquarium Architecture Slice` connect `Community 0` to `Community 16`, `Community 11`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `run_aquarium_pipeline()` connect `Community 3` to `Community 13`, `Community 6`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `run_aquarium_pipeline()` (e.g. with `RunRecord` and `run_bettafish_cli_adapter()`) actually correct?**
  _`run_aquarium_pipeline()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Locale`, `Mode`, `Stage` to the rest of the system?**
  _145 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._