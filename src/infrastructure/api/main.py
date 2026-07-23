from fastapi import FastAPI
from src.infrastructure.metrics import metrics
from src.infrastructure.api.routes import router
from src.infrastructure.middlrewares.middlrewares import metrics_middleware, log_request_middleware 
app = FastAPI(title="prediction models via API")
app.include_router(router=router)