from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    hashed_password: str

@dataclass
class InputProbabilityPrediction:
    user_id = int
    contract_name: str
    user_budget: str

@dataclass
class PredictionResult:
    prediction_id: Optional[int]
    user_input: str
    model: str
    ready_prediction: str