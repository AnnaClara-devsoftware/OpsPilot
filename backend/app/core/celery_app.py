"""Celery application factory shared by the API and the worker process."""
from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "opspilot",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.analysis_worker"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_retry_delay=10,
    task_time_limit=60 * 15,
)
