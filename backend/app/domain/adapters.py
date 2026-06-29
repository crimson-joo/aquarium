from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any

from app.domain.contracts import (
    AdapterStage,
    HandoffManifest,
    Locale,
    Ontology,
    Persona,
    SimulationMode,
    SimulationReport,
    SimulationResult,
)


def _command_env(topic: str, locale: Locale, mode: SimulationMode, run_dir: Path, manifest_path: Path | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "AQUARIUM_TOPIC": topic,
            "AQUARIUM_LOCALE": locale.value,
            "AQUARIUM_MODE": mode.value,
            "AQUARIUM_RUN_DIR": str(run_dir),
        }
    )
    if manifest_path is not None:
        env["AQUARIUM_HANDOFF_MANIFEST"] = str(manifest_path)
    return env


def _run_command(command: str, *, env: dict[str, str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        shlex.split(command),
        env=env,
        cwd=env["AQUARIUM_RUN_DIR"],
        text=True,
        capture_output=True,
        timeout=timeout,
        check=True,
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_bettafish_cli_adapter(topic: str, locale: Locale, mode: SimulationMode, run_dir: Path) -> tuple[HandoffManifest | None, AdapterStage | None]:
    command = os.environ.get("AQUARIUM_BETTAFISH_COMMAND", "").strip()
    if not command:
        return None, None

    stage = AdapterStage(name="bettafish_report", provider="bettafish_cli", status="completed")
    try:
        _run_command(
            command,
            env=_command_env(topic, locale, mode, run_dir),
            timeout=int(os.environ.get("AQUARIUM_ADAPTER_TIMEOUT_SECONDS", "900")),
        )
        manifest_path = run_dir / "bettafish_handoff_manifest.json"
        if not manifest_path.exists():
            raise RuntimeError("AQUARIUM_BETTAFISH_COMMAND did not create bettafish_handoff_manifest.json")
        manifest = HandoffManifest.model_validate(_read_json(manifest_path))
        stage.artifacts = {"handoff_manifest": str(manifest_path), "final_report": manifest.final_report_path}
        return manifest, stage
    except Exception as exc:  # pragma: no cover - failure shape is asserted through pipeline state in integration tests.
        stage.status = "failed"
        stage.warnings.append(f"BettaFish CLI adapter failed: {exc}")
        return None, stage


def run_mirofish_cli_adapter(
    topic: str,
    locale: Locale,
    mode: SimulationMode,
    run_dir: Path,
    manifest_path: Path,
) -> tuple[dict[str, Any] | None, AdapterStage | None]:
    command = os.environ.get("AQUARIUM_MIROFISH_COMMAND", "").strip()
    if not command:
        return None, None

    stage = AdapterStage(name="mirofish_simulation", provider="mirofish_cli", status="completed")
    try:
        _run_command(
            command,
            env=_command_env(topic, locale, mode, run_dir, manifest_path),
            timeout=int(os.environ.get("AQUARIUM_ADAPTER_TIMEOUT_SECONDS", "1800")),
        )
        result_path = run_dir / "mirofish_result.json"
        if not result_path.exists():
            raise RuntimeError("AQUARIUM_MIROFISH_COMMAND did not create mirofish_result.json")
        payload = _read_json(result_path)
        # Validate the payload at the adapter boundary so the main pipeline can fail loudly in tests/dev.
        Ontology.model_validate(payload["ontology"])
        [Persona.model_validate(item) for item in payload["personas"]]
        SimulationResult.model_validate(payload["simulation"])
        SimulationReport.model_validate(payload["simulation_report"])
        stage.artifacts = {"mirofish_result": str(result_path), "simulation_report": payload["simulation_report"]["path"]}
        return payload, stage
    except Exception as exc:  # pragma: no cover - failure shape is asserted through pipeline state in integration tests.
        stage.status = "failed"
        stage.warnings.append(f"MiroFish CLI adapter failed: {exc}")
        return None, stage
