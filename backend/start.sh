#!/bin/sh
set -e

alembic upgrade head

celery -A app.core.celery_app.celery_app worker --loglevel=info --concurrency=2 &

exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 2