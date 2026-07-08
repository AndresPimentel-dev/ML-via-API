# Prometheus metrics for the FastAPI app.
from time import perf_counter


from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
#from starlette.responses import Response
from fastapi import Response

from src.domain.interfaces import PredictionService, UserRepositoryInterface, PredictionRepositoryInterface, PredictionService, CacheServiceUsername, CeleryWorkersService 




# Counts all requests by method, path, and status code.
############################################################################################
ORM_OPERATIONS = Counter('orm_operations', 'lector de aperturas a la base de datos', ['type', 'table'])
ORM_LATENCY = Histogram('orm_latency', 'tiempo de respuesta de la db con el orm', ['type', 'table'])
ORM_ERRORS = Counter('orm_errors', 'lector de errores orm', ['componente','operation', 'error_type'])
class InstrumentedUserRepo(UserRepositoryInterface):
    def __init__(self, original):
        self._decored = original
    def get_by_email(self, email):
        try:
            with ORM_LATENCY.labels(type='get_by_email', table='users').time():
                ORM_OPERATIONS.labels(type='get_by_email', table='users').inc()
                return self._decored.get_by_email(email)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db',operation='get by email', error_type=type(e).__name__).inc()
            raise e
    def get_by_username(self, username):
        try:
            with ORM_LATENCY.labels(type='get_by_username', table='users').time():
                ORM_OPERATIONS.labels(type="get_by_usernma", table='users').inc()
                return self._decored.get_by_username(username)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db',operation= 'get by username', error_type=type(e).__name__).inc()
            raise e
    def create(self, username, email, hashed_password):
        try:
           with ORM_LATENCY.labels(type='create_user', table='users').time():
               ORM_OPERATIONS.labels(type='create_user', table='users').inc()
               return self._decored.create(username, email, hashed_password)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db', operation= 'create username', error_type=type(e).__name__).inc()
            raise e
        
class InstrumentedPredictionRepo(PredictionRepositoryInterface):
    def __init__(self, original):
        self._decorated = original
    def save_prediction_db(self, model_used, user_id, prediction):
        try:
           with ORM_LATENCY.labels(type='save_prediction', table='predictions').time():
               ORM_OPERATIONS.labels(type='save_prediction', table='predictions').inc()
               return self._decorated.save_prediction_db(model_used, prediction, user_id)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db',operation='save prediction', error_type=type(e).__name__).inc()
            raise e
    def get_prediction_db(self, user_id):
        try:
           with ORM_LATENCY.labels(type='get_prediction', table='predictions').time():
               ORM_OPERATIONS.labels(type='get_prediction', table='predictions').inc()
               return self._decorated.get_prediction_db(user_id)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db', error_type=type(e).__name__).inc()
            raise e
    def delete_prediction_db(self, prediction_id):
        try:
           with ORM_LATENCY.labels(type='delete_prediction', table='predictions').time():
               ORM_OPERATIONS.labels(type='delete_prediction', table='predictions').inc()
               return self._decorated.delete_prediction_db(prediction_id)
        except Exception as e:
            ORM_ERRORS.labels(componente='user repo db', operation='delete prediction', error_type=type(e).__name__).inc()
            raise e
############################################################################################

############################################################################################
CACHE_OPERATIONS = Counter('cache_operations', 'medidor uso cache', ['type'])
CACHE_LATENCY = Histogram('cache_operation_duration', 'tiempo de respuesta del cache', ['type'])
CACHE_ERRORS = Counter('cache_errors', 'contador errores cache', ['componente', 'operation', 'error_type'])
# Aquí empieza el Decorador
class InstrumentedCache(CacheServiceUsername):
    def __init__(self, original_cache):
        # Guardamos el caché real dentro del decorador
        self._decorated = original_cache

    def set_token_username(self, token: str, username: str, user_id: int,  ttl_seconds: int = 1800):
        try:
           with CACHE_LATENCY.labels(type='set').time():
               CACHE_OPERATIONS.labels(type='set').inc()
                # 2. Llamamos al método real
               return self._decorated.set_token_username(token, username, user_id, ttl_seconds)
        except Exception as e:
           CACHE_ERRORS.labels(componente='cache', operation='set username in cache', error_type=type(e).__name__).inc()
           raise e

    def get_username(self, token: str):
        try:
           with CACHE_LATENCY.labels(type='get').time():     
               CACHE_OPERATIONS.labels(type='get').inc()
               return self._decorated.get_username(token)
        except Exception as e:
            CACHE_ERRORS.labels(componente='cache', operation='get username in cache', error_type=type(e).__name__).inc()
            raise e

    def delete_username(self, token: str):
        try:
           with CACHE_LATENCY.labels(type='delete').time():
               CACHE_OPERATIONS.labels(type='delete').inc()
               return self._decorated.delete_username(token)
        except Exception as e:
            CACHE_ERRORS.labels(componente='cache', operation='delete username in cache', error_type=type(e).__name__).inc()
            raise e
############################################################################################

############################################################################################
CELERY_OPERATIONS = Counter('celery_operations', 'medidor uso trabajadores', ['type'])
CELERY_LATENCY = Histogram('celery_operation', 'tiempo de respuesta de los workers', ['type'])
CELEY_ERRORS = Counter('celery_errors', 'contador errores workers', ['type', 'error_type'])
class InstrumentedCelery(CeleryWorkersService):
    def __init__(self, original):
        self._decorated = original
    def worker_contract_provider(self, company_description: str):
        try:
           with CELERY_LATENCY.labels(type='get_contract').time():
               CELERY_OPERATIONS.labels(type='get_contract').inc()
               return self._decorated.worker_contract_provider(company_description)
        except Exception as e:
            CELEY_ERRORS.labels(type='get contract', error_type=type(e).__name__).inc()
            raise e
    def worker_probability_provider(self, contract_name, budget):
        try:
           with CELERY_LATENCY.labels(type='get_prediction').time():
               CELERY_OPERATIONS.labels(type='get_contract').inc()
               return self._decorated.worker_probability_provider(contract_name, budget)
        except Exception as e:
            CELEY_ERRORS.labels(type='get probability', error_type=type(e).__name__).inc()
############################################################################################

############################################################################################
MODEL_OPERATIONS = Counter('model_operations', 'contador uso de modelos', ['model'])
MODEL_LATENCY = Histogram('model_latency', 'medidor de lattencia de modelos', ['model'])
MODEL_ERRORS = Counter('model_errors', 'medidor errores de modelos', ['model', 'error'])
class InstrumentedModel(PredictionService):
    def __init__(self, original):
        self._decorated = original
    def get_contracts(self, company_description):
        try:
            with MODEL_LATENCY.labels(model='contratos model').time():
                MODEL_OPERATIONS.labels(model='contratos model').inc()
                return self._decorated.get_contracts(company_description)
        except Exception as e:
            MODEL_ERRORS.labels(model='contratos model', error=type(e).__name__).inc()
            raise e          
    def get_win_prediction(self, contract_name, budget):
        print({"contrato nombre en decorador": contract_name, "budget en decorador": budget})
        try:
            with MODEL_LATENCY.labels(model=' propability model').time():
                return self._decorated.get_win_prediction(contract_name, budget)
        except Exception as e:
            MODEL_ERRORS.labels(model='probability model', error=type(e).__name__).inc()
            raise e
############################################################################################

def metrics_response():
    # Return the metrics in Prometheus format.
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
#asincrona para medir mientras el resto no se para, para no afectar el rendimiento de la app, se mide el tiempo que tarda en procesar la request y se guarda en las metricas de prometheus
