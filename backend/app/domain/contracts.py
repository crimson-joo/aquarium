from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal
from pydantic import BaseModel, Field


class Locale(StrEnum):
    KO = "ko"
    ZH = "zh"
    EN = "en"


class SimulationMode(StrEnum):
    SINGLE = "single"
    MULTIVERSE = "multiverse"


class AdapterStage(BaseModel):
    name: str
    provider: str
    status: Literal["completed", "degraded", "failed"]
    artifacts: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class RunRecord(BaseModel):
    run_id: str
    topic: str
    locale: Locale
    mode: SimulationMode
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    stages: list[AdapterStage] = Field(default_factory=list)
    runtime_claim: dict[str, Any] = Field(default_factory=dict)


class HandoffManifest(BaseModel):
    handoff_version: str = "aquarium.v1"
    source_product: str = "aquarium"
    target_product: str = "aquarium"
    topic: str
    locale: Locale
    final_report_path: str
    intermediate_outputs: dict[str, str] = Field(default_factory=dict)
    sources: list[dict[str, str]] = Field(default_factory=list)
    provider: str = "local_stub"
    warnings: list[str] = Field(default_factory=list)
    data_gaps: list[str] = Field(default_factory=list)


class SeedDocument(BaseModel):
    title: str
    locale: Locale
    body: str
    key_points: list[str]


class OntologyEntity(BaseModel):
    name: str
    type: str
    rationale: str


class Ontology(BaseModel):
    entities: list[OntologyEntity]
    relations: list[dict[str, str]]


class Persona(BaseModel):
    name: str
    role: str
    stance: str


class UniverseResult(BaseModel):
    name: str
    variation: str
    dominant_signal: str
    events: list[str]


class SimulationResult(BaseModel):
    mode: SimulationMode
    universes: list[UniverseResult]


class SimulationReport(BaseModel):
    path: str
    body: str


class PipelineResult(BaseModel):
    run: RunRecord
    manifest: HandoffManifest
    seed: SeedDocument
    ontology: Ontology
    personas: list[Persona]
    simulation: SimulationResult
    simulation_report: SimulationReport
