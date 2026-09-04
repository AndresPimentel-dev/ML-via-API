from typing import Optional
import inspect
import json


from src.domain.interfaces import PredictionRepositoryInterface, CeleryWorkersService, ILogger


class PredictionService:
    def __init__(self, celery_service:CeleryWorkersService,
                 predict_repo: PredictionRepositoryInterface,
                 logger: ILogger):
        self.predict_repo = predict_repo
        self.celery_service = celery_service
        self.logger = logger

    def get_contract(self, data: dict):
        try:
            self.logger.info(message="obteniendo contratos del modelo", model_used=data["model_used and version"],user_id=data["user_id"], company_description=data["prediction"])
            prediction = self.celery_service.worker_contract_provider(company_description=data["prediction"])
            actual_data = prediction.get() 
            prediction_as_string = json.dumps(actual_data)
            self.predict_repo.save_prediction_db(model_used=data["model_used and version"], prediction=prediction_as_string, user_id=data["user_id"])
            return prediction_as_string
        except Exception as e:
            self.logger.error("fallo en proceso de obtener contrato", error=str(e), model_used=data["model_used and version"], user_id=data["user_id"], company_description=data["prediction"])
            raise e
    def get_probability_prediction(self, data: dict):
        try:
            self.logger.info("obteniendo predicion del modelo", model_used=data["model_used and version"], user_id=data["user_id"], contract_name=data["contract"], budget=data["budget"])
            prediction = self.celery_service.worker_probability_provider(contract_name=data["contract"], budget=data["budget"])
            actual_data = prediction.get()
            prediction_as_string = json.dumps(actual_data)
            return self.predict_repo.save_prediction_db(model_used=data["model_used and version"], prediction=prediction_as_string, user_id=data["user_id"])
        except Exception as e:
            self.logger.error(message="fallo al obtener prediccion",error=str(e), model_used=data["model_used and version"], user_id=data["user_id"], contract_name=data["contract"], budget=data["budget"])
            raise e
    def consult_prediction(self, user_id: int):
        try:
             self.logger.info(message="obteniendo prediccion de la db", user_id=user_id)
             predictions = self.predict_repo.get_prediction_db(user_id)
             if predictions is None:
                 return None
             return predictions
        except Exception as e:
            self.logger.error(message="error obteniendo prediccion de db", error=str(e), user_id=user_id)
            raise e
    def delete_prediction(self, prediction_id: int, owner_id: int):
        try:
            self.logger.info(message="borrando prediccion", prediction_id=prediction_id)
            delete = self.predict_repo.delete_prediction_db(prediction_id, owner_id)
            if delete is None:
                return None
            return delete
        except Exception as e:
            self.logger.error(message="error borrando predicion", error=str(e), prediction_id=prediction_id)
            raise e