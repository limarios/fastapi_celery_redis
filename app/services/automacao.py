from time import sleep
from app.core.celery_app import celery_app

@celery_app.task
def executar_automacao(cliente_id: int):
    print(f"[AUTOMAÇÃO] Iniciando para cliente {cliente_id}")
    sleep(5)  # Simula automação
    print(f"[AUTOMAÇÃO] Finalizada para cliente {cliente_id}")
    return {"cliente_id": cliente_id, "status": "concluido"}
