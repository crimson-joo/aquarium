# Release — Aquarium

## 현재 release 수준

Aquarium은 아직 public production release가 아니라, Docker Compose로 실행 가능한 local demo/research simulator입니다. 기본 `.env`는 `local_stub` degraded mode로 clone 직후 검증 가능해야 하며, real integration release 후보는 `AQUARIUM_BETTAFISH_COMMAND`와 `AQUARIUM_MIROFISH_COMMAND`가 모두 설정된 상태에서만 판정합니다.

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

- `local_stub` remains the default degraded provider and must not be reported as native/real integration.
- The current real-runner canary proves Aquarium runner contract wiring. If the MiroFish command uses a fixtured bridge, it is not evidence of live native Graphiti/OASIS execution.
- Public deployment, repo visibility changes, secrets, or cost-incurring provider setup require separate approval.
