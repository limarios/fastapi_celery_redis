from fastapi import APIRouter
from pydantic import BaseModel
from celery.result import AsyncResult
from app.services.automacao import executar_automacao
from app.core.celery_app import celery_app

router = APIRouter()

class AutomacaoInput(BaseModel):
    cliente_id: int

@router.post("/executar")
def start_automacao(payload: AutomacaoInput):
    task = executar_automacao.delay(payload.cliente_id)
    return {"status": "agendado", "task_id": task.id, }

@router.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": str(task_result.result) if task_result.ready() else None
    }
