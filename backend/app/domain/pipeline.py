from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from app.domain.adapters import run_bettafish_cli_adapter, run_mirofish_cli_adapter
from app.domain.contracts import (
    AdapterStage,
    Locale,
    Ontology,
    Persona,
    PipelineResult,
    RunRecord,
    SimulationMode,
    SimulationReport,
    SimulationResult,
)
from app.engines.graph.native import extract_ontology
from app.engines.persona.native import build_personas
from app.engines.report.native import build_simulation_report
from app.engines.research.native import build_native_manifest, build_research_report, seed_from_report
from app.engines.simulation.native import run_simulation


def _run_dir(storage_root: Path, run_id: str) -> Path:
    path = storage_root / "runs" / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_text(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)


def _write_json(path: Path, payload) -> str:
    return _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))


def _native_manifest(topic: str, locale: Locale, root: Path, warnings: list[str] | None = None):
    report = build_research_report(topic, locale)
    research_report_path = Path(_write_text(root / "research_report.md", report))
    manifest = build_native_manifest(topic, locale, research_report_path)
    stage = AdapterStage(
        name="aquarium_research",
        provider="aquarium_native",
        status="completed",
        artifacts={"final_report": str(research_report_path)},
        warnings=warnings or [],
    )
    return manifest, stage


def _native_simulation(locale: Locale, mode: SimulationMode, root: Path, seed, warnings: list[str] | None = None):
    ontology = extract_ontology(seed)
    personas = build_personas(ontology, locale)
    simulation = run_simulation(mode, seed, personas)
    simulation_report = build_simulation_report(locale, simulation, root / "simulation_report.md")
    stage = AdapterStage(
        name="aquarium_simulation",
        provider="aquarium_native",
        status="completed",
        artifacts={"simulation_report": simulation_report.path},
        warnings=warnings or [],
    )
    return ontology, personas, simulation, simulation_report, stage


def build_runtime_claim(stages: list[AdapterStage], mode: SimulationMode) -> dict[str, object]:
    """Summarize what the run can honestly claim at the API/UI boundary."""
    by_name = {stage.name: stage for stage in stages}
    providers = {name: stage.provider for name, stage in by_name.items()}
    statuses = {name: stage.status for name, stage in by_name.items()}
    warnings = [warning for stage in stages for warning in stage.warnings]
    both_aquarium_native = (
        providers.get("aquarium_research") == "aquarium_native"
        and providers.get("aquarium_simulation") == "aquarium_native"
        and statuses.get("aquarium_research") == "completed"
        and statuses.get("aquarium_simulation") == "completed"
    )
    both_real = (
        providers.get("bettafish_report") == "bettafish_cli"
        and providers.get("mirofish_simulation") == "mirofish_cli"
        and statuses.get("bettafish_report") == "completed"
        and statuses.get("mirofish_simulation") == "completed"
    )
    any_failed = any(stage.status == "failed" for stage in stages)
    any_degraded = any(stage.status == "degraded" or stage.provider == "local_stub" for stage in stages)
    native_warning = any("native_unverified" in warning or "fixture" in warning.lower() for warning in warnings)
    if any_failed:
        level = "failed"
    elif both_aquarium_native:
        level = "aquarium_native"
    elif both_real and not native_warning:
        level = "native_bounded"
    elif both_real:
        level = "real_provider_warning"
    elif any_degraded:
        level = "degraded_stub"
    else:
        level = "contract_only"
    graph_engine_status = "aquarium_native" if both_aquarium_native else ("legacy_runner" if both_real else "not_available")
    graph_memory_status = "warning" if native_warning else ("not_configured" if both_aquarium_native else ("native_pass" if both_real else "not_native"))
    return {
        "real_integration": both_real,
        "standalone_native": both_aquarium_native,
        "external_runner_dependency": both_real,
        "runtime_level": level,
        "native_bounded_smoke": (both_real and not native_warning) or both_aquarium_native,
        "degraded": any_degraded,
        "graph_engine_status": graph_engine_status,
        "graph_memory_status": graph_memory_status,
        "long_running_multiverse_verified": False,
        "mode_verified": mode.value,
        "providers": providers,
        "stage_statuses": statuses,
    }


def run_aquarium_pipeline(topic: str, locale: Locale, mode: SimulationMode, storage_root: Path, run_id: str | None = None) -> PipelineResult:
    run = RunRecord(run_id=run_id or f"aq_{uuid4().hex[:12]}", topic=topic, locale=locale, mode=mode, status="running")
    root = _run_dir(storage_root, run.run_id)

    manifest, betta_stage = run_bettafish_cli_adapter(topic, locale, mode, root)
    if manifest is None:
        native_warnings = betta_stage.warnings if betta_stage is not None else []
        manifest, native_betta_stage = _native_manifest(topic, locale, root, native_warnings)
        if betta_stage is not None:
            native_betta_stage.warnings.append("Legacy BettaFish runner failed; Aquarium native research engine produced this run instead.")
        betta_stage = native_betta_stage
    assert betta_stage is not None
    run.stages.append(betta_stage)
    manifest_path = Path(_write_json(root / "handoff_manifest.json", manifest.model_dump(mode="json")))

    report = Path(manifest.final_report_path).read_text(encoding="utf-8")
    seed = seed_from_report(topic, locale, report)

    miro_payload, miro_stage = run_mirofish_cli_adapter(topic, locale, mode, root, manifest_path)
    if miro_payload is None:
        native_warnings = miro_stage.warnings if miro_stage is not None else []
        ontology, personas, simulation, simulation_report, native_miro_stage = _native_simulation(locale, mode, root, seed, native_warnings)
        if miro_stage is not None:
            native_miro_stage.warnings.append("Legacy MiroFish runner failed; Aquarium native simulation engine produced this run instead.")
        miro_stage = native_miro_stage
    else:
        ontology = Ontology.model_validate(miro_payload["ontology"])
        personas = [Persona.model_validate(item) for item in miro_payload["personas"]]
        simulation = SimulationResult.model_validate(miro_payload["simulation"])
        simulation_report = SimulationReport.model_validate(miro_payload["simulation_report"])
    assert miro_stage is not None
    run.stages.append(miro_stage)

    run.status = "completed" if all(stage.status != "failed" for stage in run.stages) else "failed"
    run.runtime_claim = build_runtime_claim(run.stages, mode)
    result = PipelineResult(run=run, manifest=manifest, seed=seed, ontology=ontology, personas=personas, simulation=simulation, simulation_report=simulation_report)
    _write_json(root / "result.json", result.model_dump(mode="json"))
    return result
