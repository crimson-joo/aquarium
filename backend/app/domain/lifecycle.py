from __future__ import annotations

import json
import shutil
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from app.domain.contracts import Locale, SimulationMode

TERMINAL_STATUSES = {"succeeded", "failed", "cancelled"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


class LifecycleStore:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "aquarium.db"
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self) -> None:
        with self._lock, self._conn:
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL UNIQUE,
                    topic TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress INTEGER NOT NULL DEFAULT 0,
                    stage TEXT NOT NULL DEFAULT 'queued',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    cancel_requested INTEGER NOT NULL DEFAULT 0,
                    error TEXT,
                    request_json TEXT NOT NULL,
                    result_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    completed_at TEXT
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(job_id) REFERENCES jobs(job_id)
                )
            """)
            self._conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_run_id ON jobs(run_id)")
            self._conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")

    def create_job(self, topic: str, locale: Locale | str, mode: SimulationMode | str) -> dict[str, Any]:
        locale_value = locale.value if isinstance(locale, Locale) else str(locale)
        mode_value = mode.value if isinstance(mode, SimulationMode) else str(mode)
        job_id = f"job_{uuid4().hex[:12]}"
        run_id = f"aq_{uuid4().hex[:12]}"
        now = _now()
        request = {"topic": topic, "locale": locale_value, "mode": mode_value}
        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO jobs(job_id, run_id, topic, locale, mode, status, progress, stage, request_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'queued', 0, 'queued', ?, ?, ?)
                """,
                (job_id, run_id, topic, locale_value, mode_value, json.dumps(request, ensure_ascii=False), now, now),
            )
        return self.get_job(job_id)

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        return self._row_to_job(row) if row else None

    def get_job_by_run_id(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute("SELECT * FROM jobs WHERE run_id = ?", (run_id,)).fetchone()
        return self._row_to_job(row) if row else None

    def list_jobs(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._row_to_job(row) for row in rows]

    def queued_job_ids(self) -> list[str]:
        with self._lock:
            rows = self._conn.execute("SELECT job_id FROM jobs WHERE status='queued' ORDER BY created_at ASC").fetchall()
        return [row["job_id"] for row in rows]

    def recover_interrupted_jobs(self) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE jobs
                SET status='failed', progress=100, stage='interrupted', error='Worker interrupted before completion', updated_at=?, completed_at=?
                WHERE status='running'
                """,
                (_now(), _now()),
            )

    def mark_running(self, job_id: str, stage: str = "running") -> None:
        self._update(job_id, status="running", progress=10, stage=stage, attempts_increment=True, completed_at=None, error=None)

    def mark_progress(self, job_id: str, progress: int, stage: str) -> None:
        self._update(job_id, progress=progress, stage=stage)

    def mark_succeeded(self, job_id: str, result: dict[str, Any]) -> None:
        artifacts = result.get("artifacts") or {}
        with self._lock, self._conn:
            self._conn.execute(
                "UPDATE jobs SET status='succeeded', progress=100, stage='completed', result_json=?, error=NULL, updated_at=?, completed_at=? WHERE job_id=?",
                (json.dumps(result, ensure_ascii=False), _now(), _now(), job_id),
            )
            job = self.get_job(job_id)
            if job:
                self._conn.execute("DELETE FROM artifacts WHERE job_id=?", (job_id,))
                for name, path in artifacts.items():
                    self._conn.execute(
                        "INSERT INTO artifacts(artifact_id, job_id, run_id, name, path, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (f"art_{uuid4().hex[:12]}", job_id, job["run_id"], name, path, _now()),
                    )

    def mark_failed(self, job_id: str, error: str) -> None:
        self._update(job_id, status="failed", progress=100, stage="failed", error=error, completed_at=_now())

    def request_cancel(self, job_id: str) -> dict[str, Any] | None:
        job = self.get_job(job_id)
        if not job:
            return None
        if job["status"] == "queued":
            self._update(job_id, status="cancelled", progress=100, stage="cancelled", cancel_requested=1, completed_at=_now())
        elif job["status"] == "running":
            self._update(job_id, cancel_requested=1, stage="cancel_requested")
        return self.get_job(job_id)

    def is_cancel_requested(self, job_id: str) -> bool:
        job = self.get_job(job_id)
        return bool(job and job.get("cancel_requested"))

    def reset_for_retry(self, job_id: str) -> dict[str, Any] | None:
        job = self.get_job(job_id)
        if not job or job["status"] not in {"failed", "cancelled"}:
            return None
        self._update(job_id, status="queued", progress=0, stage="queued", cancel_requested=0, error=None, completed_at=None)
        return self.get_job(job_id)

    def cancel_if_requested(self, job_id: str) -> bool:
        if self.is_cancel_requested(job_id):
            self._update(job_id, status="cancelled", progress=100, stage="cancelled", completed_at=_now())
            return True
        return False

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def _update(self, job_id: str, attempts_increment: bool = False, **fields: Any) -> None:
        fields["updated_at"] = _now()
        assignments = []
        values = []
        for key, value in fields.items():
            assignments.append(f"{key}=?")
            values.append(value)
        if attempts_increment:
            assignments.append("attempts=attempts+1")
        values.append(job_id)
        with self._lock, self._conn:
            self._conn.execute(f"UPDATE jobs SET {', '.join(assignments)} WHERE job_id=?", values)

    def _row_to_job(self, row: sqlite3.Row) -> dict[str, Any]:
        job = dict(row)
        job["request"] = json.loads(job.pop("request_json"))
        result_json = job.pop("result_json")
        job["result"] = json.loads(result_json) if result_json else None
        job["cancel_requested"] = bool(job["cancel_requested"])
        return job


class JobWorker:
    def __init__(self, store: LifecycleStore, run_pipeline: Callable[..., Any], response_builder: Callable[[Any], dict[str, Any]], data_dir: Path):
        self.store = store
        self.run_pipeline = run_pipeline
        self.response_builder = response_builder
        self.data_dir = data_dir
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="aquarium-worker")
        self._inflight: set[str] = set()
        self._lock = threading.RLock()

    def enqueue(self, job_id: str) -> None:
        with self._lock:
            if job_id in self._inflight:
                return
            self._inflight.add(job_id)
        self.executor.submit(self._run_job, job_id)

    def _run_job(self, job_id: str) -> None:
        try:
            job = self.store.get_job(job_id)
            if not job or job["status"] != "queued":
                return
            if self.store.cancel_if_requested(job_id):
                return
            self.store.mark_running(job_id, "starting")
            self.store.mark_progress(job_id, 20, "research")
            if self.store.cancel_if_requested(job_id):
                return
            result = self.run_pipeline(
                job["topic"],
                Locale(job["locale"]),
                SimulationMode(job["mode"]),
                self.data_dir,
                run_id=job["run_id"],
            )
            self.store.mark_progress(job_id, 85, "persisting")
            if self.store.cancel_if_requested(job_id):
                shutil.rmtree(self.data_dir / "runs" / job["run_id"], ignore_errors=True)
                return
            self.store.mark_succeeded(job_id, self.response_builder(result))
        except Exception as exc:  # pragma: no cover - regression tests assert the API state, not traceback formatting.
            self.store.mark_failed(job_id, f"{type(exc).__name__}: {exc}")
        finally:
            with self._lock:
                self._inflight.discard(job_id)

    def shutdown(self, wait: bool = False) -> None:
        self.executor.shutdown(wait=wait, cancel_futures=True)
