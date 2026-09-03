from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv
import redis

from src.use_cases.user_cases import UserUseCases
from src.infrastructure.database.db_repository import UserRepository, PredictionsRepository
from src.use_cases.prediction_cases import PredictionService
from src.infrastructure.security.security_repository import SecurityServicesRepo, TokenService
from src.infrastructure.database.connection import get_db
from src.infrastructure.celery.celery_app import CeleryServices
from src.api.routes import oauth2_scheme
from src.infrastructure.cache.cache import CacheServices
from src.infrastructure.metrics.metrics import InstrumentedCache, InstrumentedCelery, InstrumentedUserRepo, InstrumentedPredictionRepo
from src.infrastructure.logs.logging import LokiLogger
from src.api.schemas import CurrentUser


from fastapi import Request

load_dotenv()
#deberia hacer un get para todas las variables para poder poner tests
SECRET_KEY = os.getenv("SECRET_KEY")

REDIS_URL = os.getenv("REDIS_URL")
#if REDIS_URL is None:
#    raise ValueError("¡Error crítico! La variable de entorno REDIS_URL no está definida.")


LOKI_URL = os.getenv("LOKI_URL")

ALGORITHM = "HS256"

ACCES_EXPIRE_TIME = 30

TOKEN = str

def get_cache_service():
    # Aquí creas la conexión real para producción
    
    client = redis.from_url(REDIS_URL)
    return InstrumentedCache(CacheServices(redis_client=client))

#def get_use_case(db: Session = Depends(get_db)):
#   return UserUseCases(UserRepository(db=db), SecurityService(), TokenService(SECRET_KEY=SECRET_KEY, algorithm=ALGORITHM, expire_token_time=ACCES_EXPIRE_TIME), CacheServices())

def get_use_case(
    db: Session = Depends(get_db),
    cache_service: CacheServices = Depends(get_cache_service)
):
    return UserUseCases(
        InstrumentedUserRepo(UserRepository(db=db)), 
        SecurityServicesRepo(), 
        TokenService(SECRET_KEY=SECRET_KEY, algorithm=ALGORITHM, expire_token_time=ACCES_EXPIRE_TIME), 
        cache_service,
        logger = LokiLogger(LOKI_URL)
        )

def get_prediction_case(db: Session = Depends(get_db)):
    return PredictionService(InstrumentedCelery(CeleryServices()),
                                InstrumentedPredictionRepo(PredictionsRepository(db=db)),
                                LokiLogger(LOKI_URL))

def get_token_case():
    return TokenService(SECRET_KEY=SECRET_KEY, algorithm=ALGORITHM, expire_token_time=ACCES_EXPIRE_TIME)

def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    cache_service: CacheServices = Depends(get_cache_service)
):
    # 1. Decodificar token
    service = TokenService(SECRET_KEY=SECRET_KEY, algorithm=ALGORITHM, expire_token_time=ACCES_EXPIRE_TIME)
    decode = service.decode_token(token=token)
    if not decode:
        raise HTTPException(status_code=401, detail="Token no válido o expirado")

    # 2. Intentar obtener de caché
    user_data = cache_service.get_username(token=token)
    
    # 3. Si no está en caché, buscar en DB
    if not user_data:
        print("Buscando en DB...")
        repo = InstrumentedUserRepo(UserRepository(db=db))
        user_db = repo.get_by_username(decode)
        
        if not user_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en DB")
        
        # Normalizar a dict
        user_data = {"username": user_db.username, "user_id": user_db.user_id}
        
        # Opcional: Volver a guardar en caché aquí
        # cache_service.set(token, user_data) 

    return CurrentUser(**user_data)
