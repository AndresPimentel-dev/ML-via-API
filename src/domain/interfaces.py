from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import User, InputProbabilityPrediction, PredictionResult


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_username(self, username:str):
        pass
    @abstractmethod
    def get_by_email(self, email:str):
        pass
    @abstractmethod
    def create(self, username: str, email: str, hashed_password: str):
        pass

class PredictionRepositoryInterface(ABC):
    @abstractmethod
    def save_prediction_db(model_used: str, prediction: str, user_id: int):
        pass
    @abstractmethod
    def get_prediction_db(user_id: int):
        pass
    def delete_prediction_db(prediction_id: int):
        pass

class SecurityService(ABC):
    @abstractmethod
    def hash_password(self ,plain_password:str):
        pass
    @abstractmethod
    def verify_password(self, plain_password:str, hashed_password:str):
        pass

class TokenService(ABC):
    @abstractmethod
    def create_token(self, data: dict) -> str:
        pass
    @abstractmethod
    def decode_token(token):
        pass

class CacheServiceUsername(ABC):
    @abstractmethod
    def set_token_username(self, token:str, username:str, user_id: int):
        pass
    @abstractmethod
    def get_username(self, token:str):
        pass
    @abstractmethod
    def delete_username(self, token:str):
        pass

class CeleryWorkersService(ABC):
    @abstractmethod
    def worker_contract_provider(self, company_description: str):
        pass
    @abstractmethod
    def worker_probability_provider(self, contract_name: str, budget: int):
        pass

class PredictionService(ABC):
    @abstractmethod
    def get_contracts(self, company_description:str):
        pass
    @abstractmethod
    def get_win_prediction(self, contract_name: str, budget: float):
        pass

class ILogger(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs):
        pass
    @abstractmethod
    def error(self, message: str, **kwargs):
        pass