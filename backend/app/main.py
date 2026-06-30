from __future__ import annotations

import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.core.i18n import msg
from app.domain.contracts import Locale, SimulationMode
from app.domain.lifecycle import JobWorker, LifecycleStore
from app.domain.pipeline import run_aquarium_pipeline


class CreateRunRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    locale: Locale = Locale.KO
    mode: SimulationMode = SimulationMode.SINGLE


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


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


def _job_response(job: dict):
    return {
        "job_id": job["job_id"],
        "run_id": job["run_id"],
        "topic": job["topic"],
        "locale": job["locale"],
        "mode": job["mode"],
        "status": job["status"],
        "progress": job["progress"],
        "stage": job["stage"],
        "attempts": job["attempts"],
        "cancel_requested": job["cancel_requested"],
        "error": job["error"],
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
        "completed_at": job["completed_at"],
        "result": job["result"],
        "links": {
            "job": f"/api/jobs/{job['job_id']}",
            "run": f"/api/runs/{job['run_id']}",
            "retry": f"/api/jobs/{job['job_id']}/retry",
            "resume": f"/api/jobs/{job['job_id']}/resume",
            "cancel": f"/api/jobs/{job['job_id']}/cancel",
        },
    }


def _load_run_payload(store: LifecycleStore, run_id: str):
    job = store.get_job_by_run_id(run_id)
    if job and job.get("result"):
        return job["result"]
    if job and job["status"] in {"queued", "running", "failed", "cancelled"}:
        return None
    path = _result_path(run_id)
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
        if "run" in raw:
            return {
                "run_id": raw["run"]["run_id"],
                "topic": raw["run"]["topic"],
                "locale": raw["run"]["locale"],
                "mode": raw["run"]["mode"],
                "status": raw["run"]["status"],
                "runtime_claim": raw["run"].get("runtime_claim", {}),
                "stages": raw["run"].get("stages", []),
                "artifacts": {
                    "research_report": raw["manifest"]["final_report_path"],
                    "handoff_manifest": str(_data_dir() / "runs" / run_id / "handoff_manifest.json"),
                    "simulation_report": raw["simulation_report"]["path"],
                },
                "seed": raw["seed"],
                "ecosystem": {"entities": raw["ontology"]["entities"], "relations": raw["ontology"]["relations"], "personas": raw["personas"]},
                "simulation": raw["simulation"],
                "report": {"path": raw["simulation_report"]["path"], "preview": [line for line in raw["simulation_report"]["body"].splitlines() if line.strip()][:10]},
                "summary": raw["simulation_report"]["body"].splitlines()[:6],
            }
        return raw
    return None


def create_app() -> FastAPI:
    data_dir = _data_dir()
    store = LifecycleStore(data_dir)
    store.recover_interrupted_jobs()
    worker = JobWorker(store, run_aquarium_pipeline, _run_response, data_dir)
    for queued_job_id in store.queued_job_ids():
        worker.enqueue(queued_job_id)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            worker.shutdown(wait=False)
            store.close()

    app = FastAPI(title="Aquarium API", version="0.2.0", lifespan=lifespan)
    app.state.lifecycle_store = store
    app.state.job_worker = worker

    @app.get("/api/health")
    def health():
        return {"status": "ok", "app": "Aquarium", "lifecycle": "db-backed", "worker": "enabled"}

    @app.post("/api/runs", status_code=status.HTTP_202_ACCEPTED)
    def create_run(payload: CreateRunRequest):
        job = store.create_job(payload.topic.strip(), payload.locale, payload.mode)
        worker.enqueue(job["job_id"])
        return _job_response(store.get_job(job["job_id"]))

    @app.get("/api/jobs")
    def list_jobs(limit: int = 20):
        return {"jobs": [_job_response(job) for job in store.list_jobs(max(1, min(limit, 100)))]}

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str):
        job = store.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="job not found")
        return _job_response(job)

    @app.post("/api/jobs/{job_id}/cancel")
    def cancel_job(job_id: str):
        job = store.request_cancel(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="job not found")
        return _job_response(job)

    @app.post("/api/jobs/{job_id}/retry")
    def retry_job(job_id: str):
        if not store.get_job(job_id):
            raise HTTPException(status_code=404, detail="job not found")
        job = store.reset_for_retry(job_id)
        if not job:
            raise HTTPException(status_code=409, detail="job is not retryable")
        worker.enqueue(job_id)
        return _job_response(store.get_job(job_id))

    @app.post("/api/jobs/{job_id}/resume")
    def resume_job(job_id: str):
        if not store.get_job(job_id):
            raise HTTPException(status_code=404, detail="job not found")
        job = store.reset_for_retry(job_id)
        if not job:
            raise HTTPException(status_code=409, detail="job is not resumable")
        worker.enqueue(job_id)
        return _job_response(store.get_job(job_id))

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str):
        payload = _load_run_payload(store, run_id)
        if not payload:
            raise HTTPException(status_code=404, detail="run not found")
        return payload

    @app.post("/api/runs/{run_id}/chat")
    def chat(run_id: str, payload: ChatRequest):
        result = _load_run_payload(store, run_id)
        if not result:
            raise HTTPException(status_code=404, detail="run not found")
        locale = Locale(result["locale"])
        mode = result["mode"]
        universe_count = len(result["simulation"]["universes"])
        answer = (
            f"{msg(locale, 'chat_prefix')}, 이 질문은 {universe_count}개 해류의 {mode} 시뮬레이션과 "
            f"Aquarium native 조사 seed를 함께 봐야 합니다. 핵심은 '{result['simulation']['universes'][0]['dominant_signal']}'입니다. "
            f"근거가 부족한 부분은 data_gaps에 보존되어 있습니다."
        )
        return {"run_id": run_id, "question": payload.question, "answer": answer}

    return app


app = create_app()
