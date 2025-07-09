from app.core.db import engine
from app.models.base import Base
from app.models.worker import Worker  # forçar import

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso.")