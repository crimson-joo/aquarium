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

BettaFish command는 `$AQUARIUM_RUN_DIR/bettafish_handoff_manifest.json`을 생성해야 하고, MiroFish command는 `$AQUARIUM_RUN_DIR/mirofish_result.json`을 생성해야 합니다. 자세한 계약은 [Execution Plan](docs/current/execution-plan.md)을 참고하세요.

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

현재 MVP는 실제 BettaFish/MiroFish 코드를 통째로 복사한 것이 아니라, 두 프로젝트에서 안정화한 **handoff contract와 제품 흐름**을 기준으로 만든 최소 vertical slice입니다. 실제 SearXNG/Graphiti/LLM provider adapter는 다음 단계에서 연결합니다.
