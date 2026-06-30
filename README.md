# Aquarium / 아쿠아리움

**Aquarium은 주제 하나를 native research seed → ecosystem graph → single/multiverse simulation → observation report로 바꾸는 standalone local runtime입니다.**

BettaFish-localized/MiroFish-localized repo를 옆에서 호출하는 “연결기”가 아니라, Aquarium 자체 엔진으로 조사 seed, 분류 구조(Ontology), 페르소나, 해류 시뮬레이션, 리포트/대화 흐름을 한 저장소 안에서 실행하는 방향으로 전환되었습니다. 기존 sibling runner 연결은 검증·마이그레이션용 legacy bridge로 유지됩니다.

## 현재 상태

- 한국어/중국어/영어 UI copy 기반
- 기본 실행 경로: `aquarium_native` standalone provider
- native vertical slice: topic → research seed → ontology/persona → single/multiverse simulation → report/chat
- legacy bridge: `AQUARIUM_BETTAFISH_COMMAND` / `AQUARIUM_MIROFISH_COMMAND` 외부 CLI adapter contract 지원
- FastAPI backend + Vite React frontend
- Docker Compose-first 실행 구조
- DB-backed local lifecycle: `data/aquarium.db`에 job/artifact metadata 저장, `data/runs/<run_id>/`에 보고서와 simulation artifact 저장
- job progress/stage/attempt/error/result polling과 cancel/retry/resume API/UI 제공
- API/UI가 `runtime_claim`으로 standalone/native, external runner dependency, real/degraded/native 상태를 분리 표시

## 빠른 시작

```bash
cp .env.example .env
docker compose up --build
```

접속:

- UI: http://localhost:3008
- API health: http://localhost:8008/api/health

로컬 개발 검증:

```bash
cd backend
uv sync --group dev
uv run pytest -q

cd ../frontend
npm install
npm test
npm run build
npx playwright install chromium
E2E_BASE_URL=http://127.0.0.1:3008 npm run test:e2e
```

## 기본 실행: Aquarium standalone native

clone 직후 별도 sibling repo command를 설정하지 않아도 Aquarium은 자체 native engine으로 실행됩니다.

```text
주제 입력
→ Aquarium native research seed 생성
→ ecosystem ontology/persona 추출
→ single 또는 multiverse current simulation
→ observation report
→ report/chat Q&A
```

API/UI의 `runtime_claim.runtime_level`이 `aquarium_native`이면 외부 BettaFish/MiroFish repo 호출이 아니라 Aquarium 내부 경로로 생성된 실행입니다.

`POST /api/runs`는 즉시 결과를 반환하지 않고 DB-backed job을 생성합니다. UI는 `/api/jobs/{job_id}`를 polling하여 progress/stage를 보여주고, 완료 후 seed/ecosystem/currents/report 탭을 표시합니다.

## Legacy bridge / 실제 adapter 연결

기존 BettaFish-localized/MiroFish-localized runner contract는 migration bridge로 남아 있습니다. 과거 통합 검증이나 sibling repo 비교가 필요할 때만 `.env`에 command를 지정합니다.

```bash
AQUARIUM_BETTAFISH_COMMAND="python3 /path/to/bettafish_aquarium_runner.py"
AQUARIUM_MIROFISH_COMMAND="python3 /path/to/mirofish_aquarium_runner.py"
```

BettaFish command는 `$AQUARIUM_RUN_DIR/bettafish_handoff_manifest.json`을 생성해야 하고, MiroFish command는 `$AQUARIUM_RUN_DIR/mirofish_result.json`을 생성해야 합니다. 자세한 계약은 [Execution Plan](docs/current/execution-plan.md)을 참고하세요.

legacy bridge canary:

```bash
./scripts/run_real_integration_canary.sh
```

이 canary는 두 legacy 단계가 모두 `bettafish_cli` / `mirofish_cli`이고 `completed`일 때만 `status: pass`로 종료합니다. 기본 `aquarium_native` 실행은 standalone 제품 경로로는 정상이어도, sibling-runner 실통합 canary에서는 `real_integration=false`로 남습니다. 두 상태는 서로 다른 검증 범위입니다.

## 프로젝트 문서

- [Product](docs/current/product.md)
- [Design](docs/current/design.md)
- [Architecture](docs/current/architecture.md)
- [QA](docs/current/qa.md)
- [Release](docs/current/release.md)
- [Changelog](docs/changelog.md)
- [Quickstart](docs/quickstart-ko.md)
- [Handoff Contract](docs/contracts/handoff-manifest-v1.md)

## 중요한 한계

현재 native engine은 standalone vertical slice를 완성하지만, live web search/source adapter, production Graphiti/Neo4j graph memory, 장시간 durable OASIS multiverse action stream은 아직 별도 고도화 범위입니다. UI/API는 이 한계를 `runtime_claim`과 stage warning으로 숨기지 않고 표시해야 합니다.
