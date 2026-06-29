# Aquarium Architecture Slice

BettaFish의 `topic → research report`와 MiroFish의 `seed → ontology/persona → simulation → report/chat`를 하나의 **Docker Compose-first local product**로 합치는 최소 견고(vertical slice) 제안이다.

## 1. 목표와 비목표

### 목표
- 사용자가 로컬에서 `cp .env.example .env && docker compose up --build`로 기동할 수 있다.
- MVP flow를 하나의 제품/저장소 안에서 끝까지 실행한다.
  1. topic 입력
  2. research report 생성
  3. seed document 확정
  4. ontology/persona extraction
  5. single 또는 multiverse simulation
  6. simulation report
  7. agent chat
- 초기 research/simulation provider는 deterministic/local stub로 시작 가능하지만, 실제 provider로 교체 가능한 handoff contract를 유지한다.
- 한국어/중국어/영어 i18n을 처음부터 도메인 모델, API, UI에 반영한다.
- fail-closed: 필수 provider/storage/schema가 준비되지 않으면 조용한 fallback 없이 명시적으로 실패한다.

### 비목표
- 기존 BettaFish/MiroFish 전체 복사.
- 처음부터 SearXNG, Graphiti, Neo4j, 멀티모달, 복잡한 에이전트 런타임을 모두 내장.
- production Kubernetes/Cloud 배포. GitHub 배포 가능한 로컬 제품 기준으로 시작한다.

## 2. 최소 견고 아키텍처

```text
Browser UI
  └─ Next.js frontend
      └─ FastAPI backend API
          ├─ Job orchestrator: report/simulation/chat jobs
          ├─ Provider adapters: local_stub, openai_compatible, searxng(optional), graphiti(optional)
          ├─ Contract validators: JSON Schema/Pydantic
          ├─ PostgreSQL: relational state + JSONB artifacts
          └─ File storage: ./data/artifacts mounted volume

Docker Compose
  ├─ frontend
  ├─ backend
  ├─ worker
  ├─ postgres
  └─ optional profiles: searxng, graphiti, neo4j
```

핵심 원칙:
- **Backend가 제품의 source of truth**: frontend는 job 생성/상태 조회/결과 렌더링만 담당한다.
- **Worker는 backend와 같은 코드 이미지**를 사용하되 `CMD worker`로 job loop만 실행한다.
- **PostgreSQL + artifact files**로 시작한다. Graph DB는 optional profile로 두고, MVP는 JSONB ontology/persona/simulation events로 충분히 검증한다.
- 모든 단계 산출물은 `schema_version`, `locale`, `provenance`, `quality`를 가진다.

## 3. Docker Compose 서비스

### 기본 profile
- `postgres`
  - DB: `aquarium`
  - 역할: projects, jobs, artifacts metadata, chat messages, provider calls 저장.
- `backend`
  - FastAPI.
  - REST/SSE API 제공.
  - migration 실행은 별도 command 또는 startup guard.
- `worker`
  - 같은 backend image.
  - `jobs` 테이블에서 pending job claim 후 단계 실행.
  - crash/resume 가능하도록 각 stage 결과를 artifact로 저장.
- `frontend`
  - Next.js 또는 Vite React.
  - `/`, `/runs/:id`, `/chat/:runId` 중심.

### optional profile
- `searxng`
  - 실제 web research가 필요할 때만 `--profile search`로 실행.
- `neo4j`, `graphiti`
  - graph memory 실험이 필요할 때만 `--profile graph`.
  - 기본 MVP에서는 필수 아님.

예시 command:

```bash
cp .env.example .env
docker compose up --build
# optional
docker compose --profile search up --build
```

## 4. Backend 구조

```text
backend/
  pyproject.toml
  Dockerfile
  app/
    main.py
    api/
      routes_health.py
      routes_runs.py
      routes_jobs.py
      routes_chat.py
    core/
      config.py
      i18n.py
      errors.py
      logging.py
      security.py
    db/
      session.py
      models.py
      migrations/
    domain/
      contracts/
        research_report.py
        seed_document.py
        ontology.py
        persona.py
        simulation.py
        simulation_report.py
        chat.py
      services/
        run_service.py
        artifact_service.py
        validation_service.py
    jobs/
      worker.py
      queue.py
      stages/
        research_report.py
        seed_document.py
        extraction.py
        simulation.py
        simulation_report.py
        chat_context.py
    providers/
      base.py
      llm_openai_compatible.py
      search_searxng.py
      graph_graphiti.py
      local_stub.py
    tests/
      unit/
      contract/
      integration/
```

### API 최소 세트
- `GET /health`
  - backend/db/provider readiness.
- `POST /api/runs`
  - input: `{ topic, locale, mode: "single" | "multiverse", provider_profile }`
  - output: `{ run_id, job_id }`
- `GET /api/runs/{run_id}`
  - run summary, current stage, artifact ids.
- `GET /api/jobs/{job_id}`
  - job state: pending/running/succeeded/failed/cancelled.
- `GET /api/runs/{run_id}/events`
  - SSE progress stream.
- `GET /api/artifacts/{artifact_id}`
  - report/seed/ontology/persona/simulation output.
- `POST /api/runs/{run_id}/chat`
  - input: `{ message, locale }`
  - output: answer with cited artifacts.

## 5. Frontend 구조

```text
frontend/
  package.json
  Dockerfile
  src/
    app/
      page.tsx
      runs/[runId]/page.tsx
      chat/[runId]/page.tsx
    components/
      TopicForm.tsx
      JobTimeline.tsx
      ArtifactViewer.tsx
      SimulationModeToggle.tsx
      ChatPanel.tsx
      LocaleSwitcher.tsx
    lib/
      api.ts
      i18n.ts
      schemas.ts
    messages/
      ko.json
      zh.json
      en.json
    tests/
      unit/
      e2e/
```

UI는 3 화면으로 충분하다.
- Home: topic, locale, single/multiverse, provider profile 선택.
- Run detail: job timeline + artifacts tabs.
- Chat: simulation report 기반 agent chat.

## 6. Storage 모델

### PostgreSQL 테이블
- `runs`
  - `id`, `topic`, `locale`, `mode`, `status`, `created_at`, `updated_at`.
- `jobs`
  - `id`, `run_id`, `type`, `stage`, `status`, `attempt`, `error_code`, `error_message`, `locked_at`.
- `artifacts`
  - `id`, `run_id`, `kind`, `schema_version`, `locale`, `path`, `jsonb_payload`, `quality`, `provenance`.
- `provider_calls`
  - `id`, `run_id`, `stage`, `provider`, `request_hash`, `status`, `latency_ms`, `error`.
- `chat_messages`
  - `id`, `run_id`, `role`, `locale`, `content`, `citations`, `created_at`.

### File storage
```text
data/
  artifacts/
    {run_id}/
      01_research_report.md
      01_research_report.json
      02_seed_document.json
      03_ontology.json
      04_personas.json
      05_simulation_events.jsonl
      06_simulation_report.md
      07_chat_context.json
```

정책:
- DB에는 metadata + compact JSONB.
- 긴 Markdown/JSONL은 파일에 저장하고 path를 artifact로 추적.
- artifact write는 temp file 후 atomic rename.

## 7. Job flow와 handoff contract

```text
POST /api/runs
  → create run/job
  → worker claims job
  → Stage 1 ResearchReport
  → Stage 2 SeedDocument
  → Stage 3 Ontology + Persona
  → Stage 4 Simulation(single/multiverse)
  → Stage 5 SimulationReport
  → Stage 6 ChatContext
  → run succeeded
```

### Stage 1: ResearchReport
초기 구현은 `local_stub`로 deterministic report를 만든다. 단, output schema는 실제 BettaFish 교체를 가정한다.

```json
{
  "schema_version": 1,
  "kind": "research_report",
  "topic": "...",
  "locale": "ko",
  "markdown_path": "data/artifacts/run/01_research_report.md",
  "claims": [{"text": "...", "confidence": 0.6, "citations": []}],
  "data_gaps": [],
  "quality": {"deterministic": true, "provider": "local_stub"},
  "provenance": {"source_product": "aquarium", "compatible_with": "bettafish_handoff_v1"}
}
```

### Stage 2: SeedDocument
ResearchReport를 simulation seed로 변환한다.
- `treat_as`: `scenario_research_seed_not_ground_truth`
- report의 claims/data_gaps를 분리 보존.
- seed language와 UI locale을 명시.

### Stage 3: Ontology/Persona extraction
초기 local_stub:
- ontology: topic, stakeholders, forces, uncertainties, outcomes.
- personas: 3~5명/조직 agent.
실제 LLM provider가 붙어도 같은 schema를 반환해야 한다.

### Stage 4: Simulation
- single: 하나의 timeline/events JSONL.
- multiverse: `universe_count`만큼 child simulation을 만들고 outcome cluster를 집계.
- MVP default: `mode=single`, `rounds=6`, `max_universes=3`.

### Stage 5: SimulationReport
- Markdown + structured summary.
- `citations`는 research report/seed/simulation event artifact id를 참조.

### Stage 6: Agent Chat
- Chat은 새 simulation을 돌리지 않는다.
- `chat_context.json`과 artifacts를 근거로 답한다.
- provider unavailable이면 deterministic extractive answer 또는 fail-closed 중 env로 선택하되 기본은 fail-closed.

## 8. i18n 전략

지원 locale:
- `ko`: 한국어
- `zh`: 중국어 간체 우선
- `en`: 영어

규칙:
- API는 `locale`을 BCP-47에 가깝게 저장하되 MVP는 `ko|zh|en` enum.
- artifact마다 `locale` 필수.
- provider prompt는 `system_locale`과 `output_locale`을 명시.
- UI messages는 frontend `messages/{locale}.json`.
- backend error messages는 machine code + localized message 분리.

예시 error:

```json
{
  "error_code": "PROVIDER_UNAVAILABLE",
  "message_key": "errors.providerUnavailable",
  "localized_message": "필수 provider에 연결할 수 없습니다.",
  "details": {"provider": "openai_compatible"}
}
```

## 9. Provider/env 설계

### Provider profiles
- `local_stub`
  - 기본값.
  - 네트워크/API key 없이 전체 flow 성공.
  - deterministic snapshot test 가능.
- `openai_compatible`
  - LLM 기반 report/extraction/chat.
- `searxng_openai`
  - search + LLM report.
- `graphiti_openai`
  - graph memory 연동 실험 profile.

### `.env.example`

```env
APP_ENV=local
APP_BASE_URL=http://127.0.0.1:8000
FRONTEND_BASE_URL=http://127.0.0.1:3000

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=aquarium
POSTGRES_USER=aquarium
POSTGRES_PASSWORD=aquarium

ARTIFACT_ROOT=/app/data/artifacts
DEFAULT_LOCALE=ko
SUPPORTED_LOCALES=ko,zh,en
DEFAULT_PROVIDER_PROFILE=local_stub
FAIL_CLOSED=true

JOB_POLL_INTERVAL_SECONDS=1
JOB_LOCK_TIMEOUT_SECONDS=300
MAX_SIMULATION_ROUNDS=24
MAX_MULTIVERSE_UNIVERSES=5

OPENAI_COMPATIBLE_BASE_URL=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_MODEL=

SEARXNG_BASE_URL=http://searxng:8080
GRAPHITI_BASE_URL=http://graphiti:8000
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=aquarium
```

Fail-closed checks:
- `DEFAULT_PROVIDER_PROFILE=openai_compatible`인데 key/base_url 없으면 startup 또는 first job에서 실패.
- `--profile graph`를 선택했는데 Graphiti healthcheck 실패하면 graph stage 실패.
- schema validation 실패 시 다음 stage로 진행하지 않음.

## 10. Tests 전략

### Unit tests
- Pydantic contract validation.
- i18n locale fallback 금지 확인.
- artifact atomic write/read.
- provider config fail-closed.

### Contract tests
- `research_report → seed_document` 변환.
- `seed_document → ontology/persona` 변환.
- `simulation_events → simulation_report` 변환.
- BettaFish-compatible handoff manifest v1 fixture 검증.

### Integration tests
- `docker compose up postgres backend worker` 후 API E2E.
- `local_stub` profile로 topic 입력부터 chat까지 성공.
- worker crash 후 동일 job resume/failed 상태 검증.

### E2E/UI tests
- Playwright:
  - locale switch ko/zh/en.
  - topic submit.
  - timeline stage updates.
  - report tab 렌더링.
  - chat answer with citations.

### CI 최소 세트
```text
lint backend
lint frontend
backend unit + contract tests
frontend unit tests
compose smoke with local_stub
```

## 11. Docs 구조

```text
docs/
  architecture-slice-ko.md
  quickstart-ko.md
  env-ko.md
  contracts/
    research-report-v1.md
    seed-document-v1.md
    simulation-v1.md
  adr/
    0001-compose-first.md
    0002-postgres-jsonb-before-graphdb.md
    0003-fail-closed-provider-policy.md
  runbooks/
    local-smoke.md
    provider-debug.md
```

README는 짧게 유지한다.
- 제품 한 줄 설명.
- quickstart.
- MVP flow.
- provider profile 표.
- docs 링크.

## 12. 추천 초기 파일 구조

```text
aquarium/
  README.md
  docker-compose.yml
  .env.example
  .gitignore
  Makefile
  docs/
    architecture-slice-ko.md
    quickstart-ko.md
    contracts/
  backend/
    Dockerfile
    pyproject.toml
    app/
    tests/
  frontend/
    Dockerfile
    package.json
    src/
  data/
    .gitkeep
  scripts/
    smoke_local.sh
```

## 13. Vertical slice 구현 순서

1. 저장소 skeleton + Docker Compose + PostgreSQL healthcheck.
2. Backend `POST /api/runs`, `GET /api/runs/{id}`, worker job loop.
3. `local_stub` provider로 6개 stage artifact 생성.
4. Frontend Home/Run detail/Chat 최소 UI.
5. Contract tests + compose smoke.
6. OpenAI-compatible provider adapter 추가.
7. SearXNG optional search profile 추가.
8. Graphiti/Neo4j optional graph profile 추가.

## 14. 핵심 결정

- 하나의 product 이름은 `Aquarium`; BettaFish/MiroFish는 내부 stage/provider compatibility로 흡수한다.
- 초기 MVP는 Graph DB 없이도 끝까지 돈다.
- handoff contract를 먼저 고정해 provider 교체 리스크를 낮춘다.
- deterministic local_stub를 기본값으로 두어 GitHub clone 직후 테스트 가능하게 한다.
- fail-closed를 기본으로 하여 silent fallback을 금지한다.
