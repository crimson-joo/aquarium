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


def _stub_manifest(topic: str, locale: Locale, root: Path) -> tuple[HandoffManifest, AdapterStage]:
    report = build_research_report(topic, locale)
    research_report_path = _write_text(root / "research_report.md", report)
    manifest = HandoffManifest(
        source_product="aquarium-local-stub",
        target_product="aquarium",
        topic=topic,
        locale=locale,
        final_report_path=research_report_path,
        intermediate_outputs={"query": research_report_path, "media": research_report_path, "insight": research_report_path},
        sources=[{"title": "local_stub source", "url": "local://stub", "snippet": topic}],
        data_gaps=["local_stub provider uses deterministic evidence until real BettaFish adapter is configured"],
    )
    stage = AdapterStage(
        name="bettafish_report",
        provider="local_stub",
        status="degraded",
        artifacts={"final_report": research_report_path},
        warnings=["AQUARIUM_BETTAFISH_COMMAND is not configured; using deterministic local_stub research report."],
    )
    return manifest, stage


def _stub_simulation(locale: Locale, mode: SimulationMode, root: Path, seed: SeedDocument) -> tuple[Ontology, list[Persona], SimulationResult, SimulationReport, AdapterStage]:
    ontology = extract_ontology(seed)
    personas = build_personas(ontology, locale)
    simulation = run_simulation(mode, seed, personas)
    simulation_report = build_simulation_report(locale, simulation, root / "simulation_report.md")
    stage = AdapterStage(
        name="mirofish_simulation",
        provider="local_stub",
        status="degraded",
        artifacts={"simulation_report": simulation_report.path},
        warnings=["AQUARIUM_MIROFISH_COMMAND is not configured; using deterministic local_stub simulation."],
    )
    return ontology, personas, simulation, simulation_report, stage


def run_aquarium_pipeline(topic: str, locale: Locale, mode: SimulationMode, storage_root: Path) -> PipelineResult:
    run = RunRecord(run_id=f"aq_{uuid4().hex[:12]}", topic=topic, locale=locale, mode=mode, status="running")
    root = _run_dir(storage_root, run.run_id)

    manifest, betta_stage = run_bettafish_cli_adapter(topic, locale, mode, root)
    if manifest is None:
        manifest, stub_betta_stage = _stub_manifest(topic, locale, root)
        if betta_stage is not None:
            stub_betta_stage.warnings = betta_stage.warnings + stub_betta_stage.warnings
        betta_stage = stub_betta_stage
    assert betta_stage is not None
    run.stages.append(betta_stage)
    manifest_path = Path(_write_json(root / "handoff_manifest.json", manifest.model_dump(mode="json")))

    report = Path(manifest.final_report_path).read_text(encoding="utf-8")
    seed = seed_from_report(topic, locale, report)

    miro_payload, miro_stage = run_mirofish_cli_adapter(topic, locale, mode, root, manifest_path)
    if miro_payload is None:
        ontology, personas, simulation, simulation_report, stub_miro_stage = _stub_simulation(locale, mode, root, seed)
        if miro_stage is not None:
            stub_miro_stage.warnings = miro_stage.warnings + stub_miro_stage.warnings
        miro_stage = stub_miro_stage
    else:
        ontology = Ontology.model_validate(miro_payload["ontology"])
        personas = [Persona.model_validate(item) for item in miro_payload["personas"]]
        simulation = SimulationResult.model_validate(miro_payload["simulation"])
        simulation_report = SimulationReport.model_validate(miro_payload["simulation_report"])
    assert miro_stage is not None
    run.stages.append(miro_stage)

    run.status = "completed" if all(stage.status != "failed" for stage in run.stages) else "failed"
    result = PipelineResult(run=run, manifest=manifest, seed=seed, ontology=ontology, personas=personas, simulation=simulation, simulation_report=simulation_report)
    _write_json(root / "result.json", result.model_dump(mode="json"))
    return result
