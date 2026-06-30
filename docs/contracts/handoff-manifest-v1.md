# Handoff Manifest v1

Aquarium의 handoff manifest는 Aquarium native research seed를 Aquarium simulation seed로 고정하는 계약입니다. Legacy bridge에서는 BettaFish형 research report를 MiroFish형 seed simulation으로 넘길 때도 같은 schema를 사용합니다.

## Schema

```json
{
  "handoff_version": "aquarium.v1",
  "topic": "AI 검색엔진 시장 변화",
  "locale": "ko",
  "final_report_path": "data/runs/aq_x/research_report.md",
  "intermediate_outputs": {
    "query": "...",
    "media": "...",
    "insight": "..."
  },
  "sources": [
    {"title": "source title", "url": "https://...", "snippet": "..."}
  ],
  "provider": "aquarium_native",
  "warnings": [],
  "data_gaps": ["..."]
}
```

## Policy

- manifest가 없으면 seed simulation은 blocked 상태여야 한다.
- `final_report_path`가 없거나 읽을 수 없으면 failed 상태여야 한다.
- provider가 `aquarium_native`이면 standalone 실행으로 표시한다.
- provider가 `local_stub` 또는 legacy fallback이면 결과 보고서에 data gap을 남겨야 한다.
- Graphiti/LLM/search 실패는 성공처럼 숨기지 않는다.
