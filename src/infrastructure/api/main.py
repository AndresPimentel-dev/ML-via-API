from fastapi import FastAPI
from src.infrastructure.api.routes import router
from src.infrastructure.middlrewares.middlrewares import metrics_middleware, log_request_middleware 
app = FastAPI(title="prediction models via API")
app.include_router(router=router)
@app.middleware("http")
async def metrics_middleware(request, call_next):
    # tu lógica aquí
    return await call_next(request)

@app.middleware("http")
async def log_request_middleware(request, call_next):
    # tu lógica aquí
    return await call_next(request)