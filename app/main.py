from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="API RPA com Celery")
app.include_router(router)