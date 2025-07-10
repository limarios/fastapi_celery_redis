from app.core.config import settings
from app.core.db import SessionLocal
from app.models.worker import Worker
from celery import shared_task
from datetime import datetime
import redis
import time

redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@shared_task(bind=True)
def executar_automacao(self, cliente_id: int):
    lock = redis_conn.lock("lock_automacao_global", timeout=3600)

    if not lock.acquire(blocking=False):
        print("Outra automação já está em execução. Abortando...")
        return "Em execução já existe outra automação ativa."

    db = SessionLocal()
    try:
        print(f"[AUTOMAÇÃO] Iniciando para cliente {cliente_id}")
        registro = (
            db.query(Worker)
            .filter_by(cliente_id=cliente_id, status="AGENDADO")
            .order_by(Worker.id.desc())
            .first()
        )
        if registro:
            registro.status = "EM_EXECUCAO"
            registro.data_inicio = datetime.utcnow()
            db.commit()

        time.sleep(10)  # Simula a execução

        if registro:
            registro.status = "CONCLUIDO"
            registro.data_fim = datetime.utcnow()
            db.commit()

        return f"Automação do cliente {cliente_id} concluída!"
    except Exception as e:
        if registro:
            registro.status = "FALHA"
            db.commit()
        raise e
    finally:
        db.close()
        lock.release()
