from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.core.db import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    task_id = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="AGENDADO")
    data_inicio = Column(DateTime, default=datetime.utcnow)
    data_fim = Column(DateTime, nullable=True)
    mensagem_erro = Column(Text, nullable=True)