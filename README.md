# Aquarium / 아쿠아리움

**BettaFish-style local research report → MiroFish-style seed simulation**을 하나의 직관적인 수조형 UI로 묶는 로컬 시뮬레이터입니다.

아쿠아리움은 사용자가 던진 주제를 먼저 조사 보고서로 정리하고, 그 보고서를 seed document로 삼아 ontology/persona를 만들고, 단일 해류(single) 또는 멀티버스 해류(multiverse) 시뮬레이션을 돌린 뒤, 최종 보고서와 대화형 Q&A를 제공합니다.

## 현재 MVP 상태

- 한국어/중국어/영어 UI copy 기반
- deterministic `local_stub` provider로 vertical slice 동작
- `AQUARIUM_BETTAFISH_COMMAND` / `AQUARIUM_MIROFISH_COMMAND` 기반 외부 CLI adapter contract 지원
- FastAPI backend + Vite React frontend
- Docker Compose-first 실행 구조
- BettaFish→MiroFish handoff contract 개념 반영
- single / multiverse simulation mode 지원
- 보고서와 simulation artifact를 `data/runs/<run_id>/`에 저장
- API/UI가 `runtime_claim`으로 real/degraded/native 상태를 분리 표시

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
```

## 실제 adapter 연결

기본값은 `local_stub`이며 UI/API에서 degraded 단계로 표시됩니다. 실제 BettaFish/MiroFish runner를 연결하려면 `.env`에 command를 지정합니다.

```bash
AQUARIUM_BETTAFISH_COMMAND="python3 /path/to/bettafish_aquarium_runner.py"
AQUARIUM_MIROFISH_COMMAND="python3 /path/to/mirofish_aquarium_runner.py"
```

현재 sibling repo 기준 예시는 `.env.example`에 주석으로 포함되어 있습니다. BettaFish command는 `$AQUARIUM_RUN_DIR/bettafish_handoff_manifest.json`을 생성해야 하고, MiroFish command는 `$AQUARIUM_RUN_DIR/mirofish_result.json`을 생성해야 합니다. 자세한 계약은 [Execution Plan](docs/current/execution-plan.md)을 참고하세요.

로컬 통합 canary:

```bash
./scripts/run_real_integration_canary.sh
```

이 canary는 두 단계가 모두 `bettafish_cli` / `mirofish_cli`이고 `completed`일 때만 `status: pass`로 종료합니다. 한 단계라도 `local_stub`, `degraded`, `failed`이면 JSON summary를 출력하고 exit code `2`로 끝나므로, demo fallback을 real integration으로 오해하지 않게 합니다. 단, canary는 설정된 runner command가 Aquarium 계약 산출물을 정직하게 냈는지 검증하는 로컬 계약 검증이며, command 자체의 출처/브랜치 신뢰성은 Release/Reviewer가 별도로 확인해야 합니다. Adapter subprocess에는 기본적으로 Aquarium 계약 변수와 문서화된 runner 변수만 전달되며, 추가 비밀/토큰이 꼭 필요할 때만 `AQUARIUM_RUNNER_ENV_ALLOWLIST`에 변수명을 명시합니다.

## MVP Flow

```text
주제 입력
→ BettaFish형 research report 생성
→ handoff manifest 생성
→ seed document 확정
→ ontology/persona 추출
→ single 또는 multiverse simulation
→ simulation report
→ report/chat Q&A
```

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

현재 release는 BettaFish/MiroFish 코드를 통째로 복사한 것이 아니라, 두 프로젝트의 외부 runner contract를 Aquarium에서 호출하는 방식입니다. `local_stub`는 기본 degraded mode이고, 실제 runner canary는 contract wiring과 artifact 보존을 증명합니다. 2026-06-30 기준 fake bridge 없는 live MiroFish backend + Graphiti + OASIS bounded smoke는 통과했지만, live native Graphiti/OASIS 장시간 multiverse 실행 증명은 별도 QA 범위입니다.
