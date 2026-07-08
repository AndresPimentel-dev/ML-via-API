from celery import Celery 
from dotenv import load_dotenv
import os
from src.domain.interfaces import CeleryWorkersService
from src.infrastructure.predictions.ml_repository import PredictionProvider
from src.infrastructure.metrics.metrics import InstrumentedModel
from src.infrastructure.predictions.ml_repository import PredictionProvider

load_dotenv()

RDURL = os.getenv("REDIS_URL")

celery_app = Celery(
    "task",
    #donde esta la cola de tareas
    broker=RDURL,
    #donde estan las tareas ya terminadas
    backend=RDURL
)

celery_app.conf.update(
    serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True
)

previder = InstrumentedModel(PredictionProvider())


@celery_app.task
def worker_contract_provider_task(company_description: str):
    prediction = previder.get_contracts(company_description)
    return prediction
@celery_app.task
def worker_probability_provider_task(contract_name: str, budget: float):
    print({"contrato nombre": contract_name, "budget": budget})
    print(type(budget))
    prediction = previder.get_win_prediction(contract_name, budget)
    return prediction


class CeleryServices(CeleryWorkersService):
    def worker_contract_provider(self, company_description: str):
        # Llama a la tarea decorada mediante .delay() o .apply()
        return worker_contract_provider_task.delay(company_description)
    def worker_probability_provider(self, contract_name: str, budget: int):
        return worker_probability_provider_task.delay(contract_name=contract_name, budget=budget)