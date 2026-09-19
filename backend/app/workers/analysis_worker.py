"""Celery tasks that run the analysis pipeline: scan -> metrics -> reports.

Each task updates its Job row (status/progress/logs) so the API and frontend
can poll for live progress. Failures are retried with exponential backoff and
finally marked as 'failed' with the error captured in error_message.
"""
import time
import traceback
from uuid import UUID

from celery import states
from celery.exceptions import MaxRetriesExceededError

from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.analysis import Analysis
from app.models.job import Job
from app.models.metric import Metric
from app.models.report import Report
from app.services.project_scanner import scan_project
from app.services.report_generator import generate_csv_report, generate_html_report, generate_json_report
from app.utils.safe_zip import UnsafeZipError, safe_extract

import os
import shutil
import tempfile


def _update_job(db, job: Job, **fields) -> None:
    for key, value in fields.items():
        setattr(job, key, value)
    db.commit()


def _append_log(job: Job, message: str) -> str:
    existing = job.logs or ""
    return f"{existing}{message}\n"


@celery_app.task(bind=True, max_retries=3, default_retry_delay=15)
def run_analysis_pipeline(self, job_id: str, analysis_id: str, source_path: str, is_zip: bool):
    """Full pipeline: extract (if zip) -> scan -> persist metrics -> generate reports."""
    db = SessionLocal()
    start_time = time.monotonic()
    workdir = None
    try:
        job = db.get(Job, UUID(job_id))
        analysis = db.get(Analysis, UUID(analysis_id))
        if job is None or analysis is None:
            return {"error": "job ou analysis nao encontrado"}

        job.attempts += 1
        job.status = "processing"
        job.logs = _append_log(job, "Iniciando pipeline de analise")
        db.commit()

        # 1. Prepare source directory
        if is_zip:
            workdir = tempfile.mkdtemp(prefix="opspilot_scan_")
            job.logs = _append_log(job, f"Extraindo ZIP para {workdir}")
            db.commit()
            try:
                safe_extract(source_path, workdir)
            except UnsafeZipError as exc:
                raise RuntimeError(f"ZIP invalido ou inseguro: {exc}") from exc
            root_dir = workdir
        else:
            root_dir = source_path

        # 2. Scan
        def progress_cb(percent: int, message: str):
            job.progress = percent
            job.logs = _append_log(job, message)
            db.commit()

        job.logs = _append_log(job, "Executando varredura de arquivos, metricas, TODOs e segredos")
        db.commit()
        scan_result = scan_project(root_dir, progress_callback=progress_cb)
        summary = scan_result.to_summary_dict()

        # 3. Persist analysis summary + metrics
        analysis.summary = summary
        analysis.status = "completed"
        db.commit()

        metric_rows = [
            Metric(analysis_id=analysis.id, name="total_files", value=summary["total_files"], unit="files"),
            Metric(analysis_id=analysis.id, name="total_loc", value=summary["total_loc"], unit="lines"),
            Metric(analysis_id=analysis.id, name="todo_count", value=summary["todo_count"], unit="items"),
            Metric(analysis_id=analysis.id, name="secret_count", value=summary["secret_count"], unit="items"),
            Metric(
                analysis_id=analysis.id,
                name="average_complexity_score",
                value=summary["average_complexity_score"],
                unit="score",
            ),
        ]
        db.add_all(metric_rows)
        db.commit()

        # 4. Generate reports
        reports_dir = tempfile.mkdtemp(prefix="opspilot_reports_")
        project_name = analysis.project.name if analysis.project else "Projeto"

        html_path = os.path.join(reports_dir, "report.html")
        json_path = os.path.join(reports_dir, "report.json")
        csv_path = os.path.join(reports_dir, "report.csv")

        generate_html_report(summary, html_path, project_name)
        generate_json_report(summary, json_path)
        generate_csv_report(summary, csv_path)

        db.add_all([
            Report(analysis_id=analysis.id, format="html", file_path=html_path),
            Report(analysis_id=analysis.id, format="json", file_path=json_path),
            Report(analysis_id=analysis.id, format="csv", file_path=csv_path),
        ])
        db.commit()

        job.status = "completed"
        job.progress = 100
        job.duration_seconds = round(time.monotonic() - start_time, 2)
        job.logs = _append_log(job, "Pipeline concluido com sucesso")
        db.commit()

        return {"status": "completed", "analysis_id": str(analysis.id)}

    except Exception as exc:  # noqa: BLE001
        db.rollback()
        job = db.get(Job, UUID(job_id))
        analysis = db.get(Analysis, UUID(analysis_id))
        error_text = f"{exc}\n{traceback.format_exc()}"
        if job:
            job.status = "retry"
            job.error_message = str(exc)
            job.logs = _append_log(job, f"Erro: {exc}")
            db.commit()
        try:
            raise self.retry(exc=exc)
        except MaxRetriesExceededError:
            if job:
                job.status = "failed"
                job.logs = _append_log(job, "Numero maximo de tentativas excedido")
                db.commit()
            if analysis:
                analysis.status = "failed"
                db.commit()
            return {"status": "failed", "error": str(exc)}
    finally:
        if workdir and os.path.isdir(workdir):
            shutil.rmtree(workdir, ignore_errors=True)
        db.close()
