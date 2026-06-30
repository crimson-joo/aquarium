from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

from app.core.i18n import msg
from app.domain.adapters import run_bettafish_cli_adapter, run_mirofish_cli_adapter
from app.domain.contracts import (
    AdapterStage, HandoffManifest, Locale, Ontology, OntologyEntity, Persona, PipelineResult,
    RunRecord, SeedDocument, SimulationMode, SimulationReport, SimulationResult, UniverseResult,
)

_WORD_RE = re.compile(r"[A-Za-z가-힣一-龥0-9]{2,}")


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


def _key_points(topic: str, locale: Locale) -> list[str]:
    if locale == Locale.EN:
        return [
            f"Local evidence around {topic} is treated as the research seed.",
            "Market, media, and community signals are separated before simulation.",
            "Data gaps are preserved instead of being hidden as confident findings.",
        ]
    if locale == Locale.ZH:
        return [
            f"围绕“{topic}”的本地证据被整理为研究种子。",
            "市场、媒体与社区信号在模拟前被区分。",
            "数据不足会被保留为警告，而不是伪装成确定结论。",
        ]
    return [
        f"‘{topic}’에 대한 로컬 근거를 조사 seed로 정리합니다.",
        "시장·미디어·커뮤니티 신호를 시뮬레이션 전에 분리합니다.",
        "데이터 부족 구간은 확신처럼 숨기지 않고 경고로 보존합니다.",
    ]


def build_research_report(topic: str, locale: Locale) -> str:
    points = _key_points(topic, locale)
    heading = msg(locale, "research_heading")
    return "\n\n".join([
        f"{heading}: {topic}",
        "## Key Signals" if locale == Locale.EN else ("## 核心信号" if locale == Locale.ZH else "## 핵심 신호"),
        "\n".join(f"- {point}" for point in points),
        "## Handoff Note" if locale == Locale.EN else ("## 交接说明" if locale == Locale.ZH else "## 핸드오프 메모"),
        msg(locale, "caveat"),
    ])


def seed_from_report(topic: str, locale: Locale, report: str) -> SeedDocument:
    points = [line[2:] for line in report.splitlines() if line.startswith("- ")]
    return SeedDocument(title=topic, locale=locale, body=report, key_points=points[:5])


def extract_ontology(seed: SeedDocument) -> Ontology:
    words = []
    for match in _WORD_RE.findall(seed.body):
        if match not in words and len(match) >= 2:
            words.append(match)
        if len(words) >= 5:
            break
    while len(words) < 3:
        words.append(f"Signal{len(words)+1}")
    entities = [OntologyEntity(name=word, type="Signal", rationale="seed document recurring term") for word in words[:5]]
    relations = [
        {"source": entities[i].name, "target": entities[(i + 1) % len(entities)].name, "type": "influences"}
        for i in range(min(3, len(entities)))
    ]
    return Ontology(entities=entities, relations=relations)


def build_personas(ontology: Ontology, locale: Locale) -> list[Persona]:
    labels = {
        Locale.KO: [("관찰자", "근거를 조심스럽게 검토"), ("확산자", "새로운 신호에 빠르게 반응"), ("회의론자", "데이터 부족을 강조")],
        Locale.ZH: [("观察者", "谨慎审查证据"), ("扩散者", "快速响应新信号"), ("怀疑者", "强调数据不足")],
        Locale.EN: [("Observer", "reviews evidence cautiously"), ("Amplifier", "reacts quickly to new signals"), ("Skeptic", "highlights data gaps")],
    }[locale]
    anchor = ontology.entities[0].name if ontology.entities else "seed"
    return [Persona(name=name, role=f"{anchor} persona", stance=stance) for name, stance in labels]


def run_simulation(mode: SimulationMode, seed: SeedDocument, personas: list[Persona]) -> SimulationResult:
    if mode == SimulationMode.SINGLE:
        universes = [UniverseResult(
            name="Single Current",
            variation="baseline",
            dominant_signal=seed.key_points[0],
            events=[f"{persona.name}: {persona.stance}" for persona in personas],
        )]
    else:
        variations = ["baseline current", "optimistic branch", "constraint branch"]
        universes = [
            UniverseResult(
                name=f"Universe {index + 1}",
                variation=variation,
                dominant_signal=seed.key_points[index % len(seed.key_points)],
                events=[f"round {round_no}: {personas[(round_no + index) % len(personas)].name} shifted around {variation}" for round_no in range(1, 4)],
            )
            for index, variation in enumerate(variations)
        ]
    return SimulationResult(mode=mode, universes=universes)


def build_simulation_report(locale: Locale, simulation: SimulationResult, path: Path) -> SimulationReport:
    heading = msg(locale, "simulation_heading")
    lines = [heading, "", msg(locale, "caveat"), ""]
    if simulation.mode == SimulationMode.MULTIVERSE:
        lines.append(msg(locale, "ensemble_heading"))
        lines.append(msg(locale, "ensemble_note"))
    else:
        lines.append(msg(locale, "single_heading"))
        lines.append(msg(locale, "single_note"))
    for universe in simulation.universes:
        lines.extend(["", f"### {universe.name}", f"- variation: {universe.variation}", f"- dominant signal: {universe.dominant_signal}"])
        lines.extend(f"- {event}" for event in universe.events)
    body = "\n".join(lines)
    _write_text(path, body)
    return SimulationReport(path=str(path), body=body)


def _native_manifest(topic: str, locale: Locale, root: Path, warnings: list[str] | None = None) -> tuple[HandoffManifest, AdapterStage]:
    report = build_research_report(topic, locale)
    research_report_path = _write_text(root / "research_report.md", report)
    manifest = HandoffManifest(
        source_product="aquarium-native-research",
        target_product="aquarium",
        topic=topic,
        locale=locale,
        final_report_path=research_report_path,
        intermediate_outputs={"query": research_report_path, "media": research_report_path, "insight": research_report_path},
        sources=[{"title": "Aquarium native evidence seed", "url": "aquarium://native/research", "snippet": topic}],
        provider="aquarium_native",
        data_gaps=["Native seed is deterministic/local until live source adapters are configured"],
    )
    stage = AdapterStage(
        name="aquarium_research",
        provider="aquarium_native",
        status="completed",
        artifacts={"final_report": research_report_path},
        warnings=warnings or [],
    )
    return manifest, stage


def _native_simulation(locale: Locale, mode: SimulationMode, root: Path, seed: SeedDocument, warnings: list[str] | None = None) -> tuple[Ontology, list[Persona], SimulationResult, SimulationReport, AdapterStage]:
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
    return {
        "real_integration": both_real,
        "standalone_native": both_aquarium_native,
        "external_runner_dependency": both_real,
        "runtime_level": level,
        "native_bounded_smoke": (both_real and not native_warning) or both_aquarium_native,
        "degraded": any_degraded,
        "graph_memory_status": "warning" if native_warning else ("native_pass" if both_real or both_aquarium_native else "not_native"),
        "long_running_multiverse_verified": False,
        "mode_verified": mode.value,
        "providers": providers,
        "stage_statuses": statuses,
    }


def run_aquarium_pipeline(topic: str, locale: Locale, mode: SimulationMode, storage_root: Path) -> PipelineResult:
    run = RunRecord(run_id=f"aq_{uuid4().hex[:12]}", topic=topic, locale=locale, mode=mode, status="running")
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
