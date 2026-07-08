from fastapi import Request
from src.infrastructure.logs.logging import LokiLogger
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from time import perf_counter
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

load_dotenv()

LOKI_URL = os.getenv("LOKI_URL")

logger = LokiLogger(LOKI_URL, tags={"app": "model via api"})


REQUEST_COUNT = Counter(
    #nombre metrica
    "fastapi_requests_total",
    #descip[tion metrica]
    "Total number of HTTP requests.",
    #cosas que guarda
    ["method", "path", "status"],
)

# Measures request latency.
REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)

async def metrics_middleware(request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)
    start = perf_counter()
    status_code = 500  # Valor por defecto en caso de error crítico
    path = request.scope.get("route").path if request.scope.get("route") else request.url.path
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        # Esto asegura que siempre se cuente la petición y se mida el tiempo
        duration = perf_counter() - start
        REQUEST_LATENCY.labels(request.method, path).observe(duration)
        REQUEST_COUNT.labels(request.method, path, status_code).inc()

#esta es la que recolecta los datos y se los envia a prometeus con el endpoint metrics
#no importa donde la cree o corra ella ya conoce en donde estan todos los counter en general sin necesidad de importarlos

async def log_request_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Aquí usamos el logger ya instanciado
        logger.error("Error en request", path=request.url.path, error=str(e))
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error inesperado"}
        )