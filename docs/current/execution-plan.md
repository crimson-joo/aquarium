# Aquarium 실행계획 — stub MVP에서 실제 BettaFish→MiroFish 통합 제품까지

## 목표

아쿠아리움은 사용자가 주제를 입력하면 BettaFish-localized가 로컬 조사 보고서를 만들고, 그 보고서가 MiroFish-localized의 seed가 되어 분류 구조(Ontology), 페르소나, single/multiverse 시뮬레이션, 최종 리포트와 보고서 AI(Report Agent) 대화까지 이어지는 로컬 우선 시뮬레이터다.

## 현재 완료 상태

- 신규 repo, Docker Compose, backend/frontend, docs/current, CI, Graphify가 준비되어 있다.
- 기본 vertical slice는 `local_stub`로 동작한다.
- 이번 단계에서 실제 엔진 연결을 위한 CLI adapter contract가 추가되었다.
- API/UI는 각 단계가 `local_stub`, `bettafish_cli`, `mirofish_cli` 중 무엇으로 실행됐는지 표시한다.

## 실행 단계

### Phase 1 — Adapter contract 고정

완료 기준:

- `AQUARIUM_BETTAFISH_COMMAND`가 설정되면 Aquarium이 외부 BettaFish runner를 호출한다.
- BettaFish runner는 run directory에 `bettafish_handoff_manifest.json`을 쓴다.
- Aquarium은 그 manifest의 `final_report_path`를 seed document로 사용한다.
- `AQUARIUM_MIROFISH_COMMAND`가 설정되면 Aquarium이 외부 MiroFish runner를 호출한다.
- MiroFish runner는 run directory에 `mirofish_result.json`을 쓴다.
- Aquarium은 ontology/persona/simulation/report를 외부 결과로 대체한다.
- 미설정 상태에서는 `local_stub`로 degraded 상태를 명확히 표시한다.

### Phase 2 — BettaFish 실제 report 연결

완료 기준:

- BettaFish-localized 쪽에 Aquarium용 runner를 추가하거나 기존 canary/handoff runner를 연결한다.
- runner는 환경변수 `AQUARIUM_TOPIC`, `AQUARIUM_LOCALE`, `AQUARIUM_RUN_DIR`를 읽는다.
- 실제 final Markdown/HTML report와 handoff manifest를 생성한다.
- 한국어 모드에서 중국어 template leakage가 없어야 한다.
- data gaps는 보고서/manifest에서 숨기지 않는다.

### Phase 3 — MiroFish 실제 simulation 연결

완료 기준:

- MiroFish-localized 쪽에 Aquarium용 runner를 추가하거나 기존 bridge runner를 연결한다.
- runner는 `AQUARIUM_HANDOFF_MANIFEST`를 읽는다.
- ontology/project/graph/persona/single 또는 multiverse simulation/report를 생성한다.
- Graphiti/native graph memory 실패는 전체 성공으로 숨기지 않고 warning/status로 표시한다.
- 결과는 `mirofish_result.json`으로 Aquarium에 전달한다.

### Phase 4 — UI/UX 제품화

완료 기준:

- 단계별 진행상태가 사용자에게 보인다.
- 각 단계의 provider, status, warning, artifact가 보인다.
- 한국어 기본 UX를 유지하고, 중국어/영어는 선택 언어로만 동작한다.
- 보고서, ontology, persona, universe comparison, chat panel을 탭으로 분리한다.

### Phase 5 — 배포 품질

완료 기준:

- Docker Compose profiles를 `minimal`, `local-search`, `graph-memory`, `full`로 정리한다.
- `.env.example`에 adapter command 예시가 포함된다.
- README quickstart가 실제 adapter 연결과 stub 모드를 구분한다.
- CI와 local compose smoke가 통과한다.

## Adapter command contract

### BettaFish command

입력 환경변수:

```text
AQUARIUM_TOPIC
AQUARIUM_LOCALE
AQUARIUM_MODE
AQUARIUM_RUN_DIR
```

출력 파일:

```text
$AQUARIUM_RUN_DIR/bettafish_handoff_manifest.json
```

필수 manifest 필드:

```json
{
  "handoff_version": "aquarium.v1",
  "source_product": "bettafish-localized",
  "target_product": "aquarium",
  "topic": "...",
  "locale": "ko",
  "final_report_path": "...",
  "provider": "bettafish_cli",
  "warnings": [],
  "data_gaps": []
}
```

### MiroFish command

입력 환경변수:

```text
AQUARIUM_TOPIC
AQUARIUM_LOCALE
AQUARIUM_MODE
AQUARIUM_RUN_DIR
AQUARIUM_HANDOFF_MANIFEST
```

출력 파일:

```text
$AQUARIUM_RUN_DIR/mirofish_result.json
```

필수 result 필드:

```json
{
  "provider": "mirofish_cli",
  "ontology": {"entities": [], "relations": []},
  "personas": [],
  "simulation": {"mode": "single", "universes": []},
  "simulation_report": {"path": "...", "body": "..."},
  "warnings": []
}
```

## 다음 작업 추천

바로 다음 목표는 Phase 2다. 즉 Aquarium repo 내부 작업이 아니라, BettaFish-localized에 Aquarium runner를 추가/연결하고 Aquarium에서 `AQUARIUM_BETTAFISH_COMMAND`로 실제 report를 생성하는 것이다.
