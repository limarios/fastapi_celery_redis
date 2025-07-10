import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)

def obter_lock(nome_lock: str, timeout: int = 3600):
    """
    Cria e retorna um lock redis com nome e timeout definidos.
    """
    return redis_client.lock(nome_lock, timeout=timeout)
