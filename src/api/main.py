from fastapi import FastAPI
from src.infrastructure.metrics import metrics
from src.api.routes import router
app = FastAPI(title="prediction models via API")
app.include_router(router=router)