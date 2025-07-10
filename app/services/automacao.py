from celery import shared_task
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.worker import Worker
from app.core.config import settings
from datetime import datetime
import redis
import time

# Conexão Redis para Lock
redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@shared_task(name="automacao.executar")
def executar_automacao(cliente_id: int):
    # Lock global para garantir uma automação por vez
    lock = redis_conn.lock("lock_automacao_global", timeout=3600)

    if not lock.acquire(blocking=False):
        print("[LOCK] Já existe uma automação em execução. Abortando...")
        return

    db: Session = next(get_db())

    try:
        print(f"[AUTOMAÇÃO] Iniciando para cliente {cliente_id}")

        # Obter o registro mais recente AGENDADO
        registro = db.query(Worker).filter_by(cliente_id=cliente_id, status="AGENDADO") \
            .order_by(Worker.id.desc()).first()

        if not registro:
            print(f"[AUTOMAÇÃO] Nenhuma automação AGENDADA para cliente {cliente_id}")
            return

        # Simula uma automação demorada
        time.sleep(300)

        # Atualiza o status para CONCLUIDO
        registro.status = "CONCLUIDO"
        registro.data_fim = datetime.utcnow()
        db.commit()

        print(f"[AUTOMAÇÃO] Finalizada para cliente {cliente_id}")

    except Exception as e:
        print(f"[ERRO] {e}")
        if registro:
            registro.status = "FALHA"
            registro.data_fim = datetime.utcnow()
            db.commit()
    finally:
        db.close()
        lock.release()
