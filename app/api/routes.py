from fastapi import APIRouter
from pydantic import BaseModel
from app.services.automacao import executar_automacao

router = APIRouter()

class AutomacaoInput(BaseModel):
    cliente_id: int

@router.post("/executar")
def start_automacao(payload: AutomacaoInput):
    task = executar_automacao.delay(payload.cliente_id)
    return {"status": "agendado", "task_id": task.id}