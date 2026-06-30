#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
DATA_DIR="${AQUARIUM_CANARY_DATA_DIR:-${ROOT_DIR}/.hermes/runs/real-integration-canary/data}"
TOPIC="${AQUARIUM_CANARY_TOPIC:-Aquarium real runner integration canary}"
LOCALE="${AQUARIUM_CANARY_LOCALE:-ko}"
MODE="${AQUARIUM_CANARY_MODE:-single}"

mkdir -p "${DATA_DIR}"
cd "${ROOT_DIR}/backend"

AQUARIUM_CANARY_DATA_DIR="${DATA_DIR}" \
AQUARIUM_CANARY_TOPIC="${TOPIC}" \
AQUARIUM_CANARY_LOCALE="${LOCALE}" \
AQUARIUM_CANARY_MODE="${MODE}" \
uv run python - <<'PY'
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from app.domain.contracts import Locale, SimulationMode
from app.domain.pipeline import run_aquarium_pipeline


def main() -> int:
    data_dir = Path(os.environ["AQUARIUM_CANARY_DATA_DIR"])
    topic = os.environ["AQUARIUM_CANARY_TOPIC"]
    locale = Locale(os.environ["AQUARIUM_CANARY_LOCALE"])
    mode = SimulationMode(os.environ["AQUARIUM_CANARY_MODE"])

    result = run_aquarium_pipeline(topic, locale, mode, data_dir)
    stages = {stage.name: stage for stage in result.run.stages}
    providers = {name: stage.provider for name, stage in stages.items()}
    stage_statuses = {name: stage.status for name, stage in stages.items()}
    warnings: list[str] = []
    artifacts: dict[str, str] = {}
    for stage in result.run.stages:
        warnings.extend(stage.warnings)
        artifacts.update({f"{stage.name}.{key}": value for key, value in stage.artifacts.items()})

    run_dir = data_dir / "runs" / result.run.run_id
    real_integration = (
        providers.get("bettafish_report") == "bettafish_cli"
        and providers.get("mirofish_simulation") == "mirofish_cli"
        and stage_statuses.get("bettafish_report") == "completed"
        and stage_statuses.get("mirofish_simulation") == "completed"
    )
    summary = {
        "status": "pass" if real_integration else "degraded",
        "real_integration": real_integration,
        "runtime_claim": result.run.runtime_claim,
        "run_id": result.run.run_id,
        "topic": result.run.topic,
        "locale": result.run.locale.value,
        "mode": result.run.mode.value,
        "providers": providers,
        "stage_statuses": stage_statuses,
        "warnings": warnings,
        "artifacts": artifacts,
        "result_path": str(run_dir / "result.json"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if real_integration else 2


try:
    raise SystemExit(main())
except Exception as exc:
    print(json.dumps({"status": "failed", "real_integration": False, "error": str(exc)}, ensure_ascii=False, indent=2))
    raise SystemExit(1)
PY
