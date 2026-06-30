from __future__ import annotations

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.i18n import msg
from app.domain.contracts import Locale, SimulationMode
from app.domain.pipeline import run_aquarium_pipeline


class CreateRunRequest(BaseModel):
    topic: str
    locale: Locale = Locale.KO
    mode: SimulationMode = SimulationMode.SINGLE


class ChatRequest(BaseModel):
    question: str


def _data_dir() -> Path:
    path = get_settings().data_dir
    path.mkdir(parents=True, exist_ok=True)
    return path


def _result_path(run_id: str) -> Path:
    return _data_dir() / "runs" / run_id / "result.json"


def _run_response(result):
    return {
        "run_id": result.run.run_id,
        "topic": result.run.topic,
        "locale": result.run.locale,
        "mode": result.run.mode,
        "status": result.run.status,
        "runtime_claim": result.run.runtime_claim,
        "stages": [stage.model_dump(mode="json") for stage in result.run.stages],
        "artifacts": {
            "research_report": result.manifest.final_report_path,
            "handoff_manifest": str(_data_dir() / "runs" / result.run.run_id / "handoff_manifest.json"),
            "simulation_report": result.simulation_report.path,
        },
        "seed": result.seed.model_dump(mode="json"),
        "ecosystem": {
            "entities": [entity.model_dump(mode="json") for entity in result.ontology.entities],
            "relations": result.ontology.relations,
            "personas": [persona.model_dump(mode="json") for persona in result.personas],
        },
        "simulation": result.simulation.model_dump(mode="json"),
        "report": {
            "path": result.simulation_report.path,
            "preview": [line for line in result.simulation_report.body.splitlines() if line.strip()][:10],
        },
        "summary": result.simulation_report.body.splitlines()[:6],
    }


def create_app() -> FastAPI:
    app = FastAPI(title="Aquarium API", version="0.1.0")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "app": "Aquarium"}

    @app.post("/api/runs")
    def create_run(payload: CreateRunRequest):
        result = run_aquarium_pipeline(payload.topic, payload.locale, payload.mode, _data_dir())
        return _run_response(result)

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str):
        path = _result_path(run_id)
        if not path.exists():
            raise HTTPException(status_code=404, detail="run not found")
        return json.loads(path.read_text(encoding="utf-8"))

    @app.post("/api/runs/{run_id}/chat")
    def chat(run_id: str, payload: ChatRequest):
        path = _result_path(run_id)
        if not path.exists():
            raise HTTPException(status_code=404, detail="run not found")
        result = json.loads(path.read_text(encoding="utf-8"))
        locale = Locale(result["run"]["locale"])
        mode = result["run"]["mode"]
        universe_count = len(result["simulation"]["universes"])
        answer = (
            f"{msg(locale, 'chat_prefix')}, 이 질문은 {universe_count}개 해류의 {mode} 시뮬레이션과 "
            f"Aquarium native 조사 seed를 함께 봐야 합니다. 핵심은 '{result['simulation']['universes'][0]['dominant_signal']}'입니다. "
            f"근거가 부족한 부분은 data_gaps에 보존되어 있습니다."
        )
        return {"run_id": run_id, "question": payload.question, "answer": answer}

    return app


app = create_app()
