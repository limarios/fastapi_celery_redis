from datetime import datetime
from time import sleep
from app.core.celery_app import celery_app
from app.core.db import SessionLocal
from app.models.worker import Worker

@celery_app.task
def executar_automacao(cliente_id: int):
    db = SessionLocal()
    try:
        print(f"[AUTOMAÇÃO] Iniciando para cliente {cliente_id}")
        registro = db.query(Worker).filter_by(cliente_id=cliente_id, status="AGENDADO").order_by(Worker.id.desc()).first()
        if registro:
            registro.status = "CONCLUIDO"
            registro.data_fim = datetime.utcnow()
            db.commit()
        sleep(5)
        print(f"[AUTOMAÇÃO] Finalizada para cliente {cliente_id}")
        return {"cliente_id": cliente_id, "status": "concluido"}
    finally:
        db.close()