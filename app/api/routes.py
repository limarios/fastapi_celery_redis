from fastapi import APIRouter, Depends
from pydantic import BaseModel
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.services.automacao import executar_automacao
from app.core.db import get_db, Session
from app.models.worker import Worker

router = APIRouter()

class AutomacaoInput(BaseModel):
    cliente_id: int

@router.post("/executar")
def start_automacao(payload: AutomacaoInput, db: Session = Depends(get_db)):
    task = executar_automacao.delay(payload.cliente_id)

    registro = Worker(
        cliente_id=payload.cliente_id,
        task_id=task.id,
        status="AGENDADO"
    )
    db.add(registro)
    db.commit()

    return {
        "status": "agendado",
        "task_id": task.id,
        "cliente_id": payload.cliente_id
    }

@router.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": str(task_result.result) if task_result.ready() else None
    }

@router.get("/automacoes/{cliente_id}")
def listar_automacoes(cliente_id: int, db: Session = Depends(get_db)):
    registros = db.query(Worker).filter_by(cliente_id=cliente_id).all()
    return [
        {
            "task_id": r.task_id,
            "status": r.status,
            "data_inicio": r.data_inicio,
            "data_fim": r.data_fim
        } for r in registros
    ]
