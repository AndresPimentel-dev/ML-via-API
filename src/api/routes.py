from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

from src.api.schemas import UserCreate, TokenResponse, StatusResponse, ProbabilityInput, ContractServiceInput, StatusResponse
from src.use_cases.user_cases import UserUseCases
from src.use_cases.prediction_cases import Predictioncasescreator
from src.domain.entities import User
from src.api.dependencies import get_current_user, get_prediction_case, get_use_case



router = APIRouter()



###############
#endpoints de health y metricts
##############
@router.get("/health/live")
def health():
    return {"status": "ok"}



@router.get("/metrics")
def metrics():
    # generate_latest retorna bytes, CONTENT_TYPE_LATEST es 'text/plain; version=0.0.4'
    return Response(
        content=generate_latest(), 
        media_type=CONTENT_TYPE_LATEST
    )

###############
#endpoints de autenticacion
##############

@router.post("/api/v1/auth/register", status_code=201, response_model=TokenResponse)
def register(user: UserCreate, user_case: UserUseCases = Depends(get_use_case)):
    new_user = user_case.register_user(username=user.username, email=user.email, plain_password=user.password)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    return {"access_token": new_user, "token_type": "bearer"}

@router.post("/api/v1/auth/login", status_code=200, response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), use_case: UserUseCases = Depends(get_use_case)):
    user = use_case.login_user(username=form.username, plain_password=form.password)
    if not user:
        raise  HTTPException(status_code=400, detail="INCORRECT")
    #que sea acces token o si no el candado no lo lee
    return {"access_token": user, "token_type": "bearer"}

##############################
#endpoints de uso
##############################

@router.post("/api/v1/predictions/contracts", status_code=201, response_model=StatusResponse)
def create_prediction(
    data: ContractServiceInput,
    username = Depends(get_current_user), # <--- Aquí está la seguridad
    prediction_case: Predictioncasescreator = Depends(get_prediction_case)
):
    print(username)
    prediction_case.get_contract({"model_used": "contract_provider_model", "prediction": data.company_description, "user_id": username.user_id})
    
    return {"status": "Predicción creada y guardada"}

@router.post("/api/v1/predictions/probability", status_code=201, response_model=StatusResponse)
def get_probability(
    data: ProbabilityInput,
    username = Depends(get_current_user),
    prediction_case: Predictioncasescreator = Depends(get_prediction_case)
):
    prediction_case.get_probability_pred({"model_used": "probability_provider_model", "contract": data.contract_name,"budget": data.user_budget, "user_id": username.user_id})
    return {"status": "Predicción creada y guardada"}

@router.get("/api/v1/predictions", status_code=200)
def obtenerprediccion(
    username = Depends(get_current_user),
    user_case: Predictioncasescreator = Depends(get_prediction_case)):
    predictions = user_case.consult_prediction(username.user_id)
    print(predictions)
    print(type(predictions))
    return {"user_creator": username.username, "prediction": predictions}

@router.delete("/api/v1/predictions/{prediction_id}", status_code=200, response_model=StatusResponse)
def borrar_prediccion(
    prediction_id:int,
    username = Depends(get_current_user),
    use_case: Predictioncasescreator = Depends(get_prediction_case)
):
    use_case.delete_prediction(prediction_id, username.user_id)
    return {"status": "tarea borrada"}