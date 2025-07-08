from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery_app.autodiscover_tasks(['app.services'])

celery_app.conf.update(
    task_track_started=True,
    task_ignore_result=False,
    result_expires=3600,  # mantém resultado por 1 hora
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)