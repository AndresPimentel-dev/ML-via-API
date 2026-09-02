from pydantic import BaseModel, ConfigDict
from typing import List

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ContractServiceInput(BaseModel):
    company_description: str

class ProbabilityInput(BaseModel):
    contract_name: str
    user_budget: float

class StatusResponse(BaseModel):
    status: str

class CurrentUser(BaseModel):
    username: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class StatusResponse(BaseModel):
    status: str