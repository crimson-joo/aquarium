# Release — Aquarium

## 현재 release 수준

Aquarium은 public hosted SaaS production release가 아니라, Docker Compose로 실행 가능한 standalone local research/simulation runtime입니다. 기본 `.env`는 `aquarium_native` provider로 clone 직후 실행 가능해야 하며, `AQUARIUM_BETTAFISH_COMMAND`와 `AQUARIUM_MIROFISH_COMMAND`는 legacy sibling-runner canary가 필요할 때만 설정합니다.

Standalone native vertical slice는 Aquarium repo 자체에서 동작합니다. 과거 BettaFish-localized/MiroFish-localized 외부 runner contract release evidence는 legacy bridge로 보존되어 있고, 2026-06-30 추가 QA에서 fake bridge 없이 live MiroFish backend + Graphiti + OASIS bounded single-run smoke도 통과했습니다. 다만 장시간 multiverse/native production run은 아직 별도 검증 범위입니다.

## 현재 기본 실행 경로

```text
docker compose up --build
→ Aquarium UI
→ aquarium_native research/simulation engines
→ runtime_claim.standalone_native=true
```

## Legacy sibling-runner 통합 실행 경로

실제 runner 연결은 Aquarium repo 안에서 두 command를 `.env`에 지정하는 방식입니다.

```bash
AQUARIUM_BETTAFISH_COMMAND="python3 /Users/crimson/Projects/bettafish-localized/scripts/bettafish_aquarium_runner.py"
AQUARIUM_MIROFISH_COMMAND="python3 /Users/crimson/Projects/mirofish-localized/scripts/mirofish_aquarium_runner.py"
./scripts/run_real_integration_canary.sh
```

- BettaFish command는 `AQUARIUM_TOPIC`, `AQUARIUM_LOCALE`, `AQUARIUM_MODE`, `AQUARIUM_RUN_DIR`를 받아 `$AQUARIUM_RUN_DIR/bettafish_handoff_manifest.json`을 생성해야 합니다.
- MiroFish command는 위 변수와 `AQUARIUM_HANDOFF_MANIFEST`를 받아 `$AQUARIUM_RUN_DIR/mirofish_result.json`을 생성해야 합니다.
- 두 단계가 모두 `bettafish_cli completed` / `mirofish_cli completed`일 때만 real integration PASS입니다.
- API/UI는 `runtime_claim`으로 `standalone_native`, `external_runner_dependency`, `real_integration`, `runtime_level`, `graph_engine_status`, `graph_memory_status`, `long_running_multiverse_verified`를 함께 표시합니다. `aquarium_native`는 standalone vertical slice, `graph_engine_status=aquarium_native`는 Aquarium 자체 생태계 지도 생성, `graph_memory_status=not_configured`는 Graphiti 기억 계층 미연결을 뜻합니다. `native_bounded`는 legacy bridge를 통한 bounded native smoke 통과를 뜻하며, `long_running_multiverse_verified=false`인 동안 production 장시간 native라고 부르지 않습니다.

## Local release gate

```bash
cd backend && uv run pytest -q
cd ../frontend && npm test && npm run build
cd .. && docker compose config  # or docker-compose config when the Docker CLI compose plugin is unavailable
./scripts/run_real_integration_canary.sh
```

`run_real_integration_canary.sh`는 실제 runner가 모두 연결된 release 후보에서만 exit code `0`이어야 합니다. runner가 비어 있거나 한 단계라도 degraded/fallback이면 exit code `2`가 정상적인 “real integration 미충족” 신호입니다.

## GitHub Actions contract

- Workflow: `.github/workflows/validate.yml`
- Triggers: `push` to `main`/`develop`, `pull_request` to `main`/`develop`
- Required release check candidate: `Local Runtime CI / validate`
- CI commands:
  - `backend`: `uv sync --group dev`, `uv run pytest -q`
  - `frontend`: `npm ci`, `npm test`, `npm run build`
  - repo root: `docker compose config --quiet`
- Deployment: none. GitHub Actions currently validates local runtime readiness only; it does not publish a public URL.

## Docker endpoints

- Frontend: `http://localhost:3008`
- Backend: `http://localhost:8008`
- Health: `http://localhost:8008/api/health`

## Release caveats

- `aquarium_native` is the default standalone provider and must not be confused with sibling-runner `real_integration`.
- `AQUARIUM_BETTAFISH_COMMAND`와 `AQUARIUM_MIROFISH_COMMAND`를 지정하면 Aquarium은 legacy external runner contract를 호출합니다.
- 현재 release evidence는 BettaFish runner contract + MiroFish runner contract + Aquarium canary wiring을 증명합니다.
- 2026-06-30 native canary evidence는 live MiroFish backend, Graphiti native graph build/search, OASIS parallel simulation, Korean report generation까지 bounded single run으로 증명합니다.
- 2026-06-30 multiverse expansion evidence는 MiroFish live endpoint preflight + bounded real-backend multiverse comparison을 증명합니다: `mv_4ef846551b2d`, 4 universes, 24 configured rounds, graph memory preflight healthy, 3 outcome clusters, 4 sensitivity axes.
- 장시간 durable OASIS action stream 기반 multiverse production run, public deployment, repo visibility changes, secrets, or cost-incurring provider setup require separate approval.

## Released PRs

- Aquarium develop→main: https://github.com/crimson-joo/aquarium/pull/1
- BettaFish-localized develop→main: https://github.com/crimson-joo/bettafish-localized/pull/16
- MiroFish-localized develop→main: https://github.com/crimson-joo/mirofish-localized/pull/48
