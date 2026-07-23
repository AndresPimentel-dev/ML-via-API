import pytest
import json
import redis
from unittest.mock import MagicMock
from src.infrastructure.cache.cache import CacheServices

@pytest.fixture
def mock_redis():
    """Crea un cliente de Redis falso."""
    return MagicMock()

@pytest.fixture
def cache_service(mock_redis):
    """Crea la instancia del servicio inyectando el cliente falso."""
    return CacheServices(redis_client=mock_redis)

# --- TESTS ---

def test_set_token_username_success(cache_service, mock_redis):
    # Act
    cache_service.set_token_username("token123", "usuario1", 100)
    
    # Assert
    # Verificamos que se llamó a Redis con los datos correctos
    mock_redis.set.assert_called_once()
    args, kwargs = mock_redis.set.call_args
    assert args[0] == "user:token123"
    assert "username" in args[1]  # Verifica que es un JSON

def test_set_token_username_redis_fails(cache_service, mock_redis):
    # Simulamos que Redis lanza un error
    mock_redis.set.side_effect = redis.RedisError("Error de conexión")
    
    # Act
    cache_service.set_token_username("token123", "usuario1", 100)
    
    # Assert
    # Debería haber guardado en el fallback local
    assert cache_service._local_fallback["token123"] is not None

def test_get_username_success(cache_service, mock_redis):
    # Arrange
    mock_data = json.dumps({"username": "usuario1", "user_id": 1})
    mock_redis.get.return_value = mock_data
    
    # Act
    resultado = cache_service.get_username("token123")
    
    # Assert
    assert resultado["username"] == "usuario1"
    mock_redis.get.assert_called_once_with("user:token123")

def test_delete_username(cache_service, mock_redis):
    # Act
    cache_service.delete_username("token123")
    
    # Assert
    mock_redis.delete.assert_called_once_with("user:token123")

import pytest
from unittest.mock import patch, MagicMock
# Importas tus tareas
from src.infrastructure.celery.celery_app import worker_contract_provider_task, worker_probability_provider_task

# Usamos patch para sustituir el 'previder' global que está en tu archivo de tareas
@patch('src.infrastructure.celery.celery_app.previder')
def test_worker_contract_provider_task(mock_previder):
    # 1. Configuras el mock (simulas lo que devuelve el modelo de ML)
    mock_previder.get_contracts.return_value = ["Contrato A", "Contrato B"]
    
    # 2. Llamas a la tarea como si fuera una función normal
    resultado = worker_contract_provider_task("descripcion de empresa")
    
    # 3. Verificas
    assert resultado == ["Contrato A", "Contrato B"]
    mock_previder.get_contracts.assert_called_once_with("descripcion de empresa")

@patch('src.infrastructure.celery.celery_app.previder')
def test_worker_probability_provider_task(mock_previder):
    # 1. Configuras el mock
    mock_previder.get_win_prediction.return_value = 0.85
    
    # 2. Llamas a la tarea
    resultado = worker_probability_provider_task("Nombre Contrato", 5000.0)
    
    # 3. Verificas
    assert resultado == 0.85
    mock_previder.get_win_prediction.assert_called_once_with("Nombre Contrato", 5000.0)

import pytest
from unittest.mock import MagicMock
from src.infrastructure.database.db_repository import UserRepository # Ajusta la ruta

@pytest.fixture
def mock_db():
    return MagicMock()

def test_get_by_username_found(mock_db):
    # 1. Configuramos el mock de la cadena: query -> filter -> first
    mock_user = MagicMock()
    mock_user.username = "testuser"
    
    # Aquí simulamos: db.query(...).filter(...).first()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    repo = UserRepository(mock_db)
    result = repo.get_by_username("testuser")

    # 2. Verificamos
    assert result.username == "testuser"
    mock_db.query.assert_called() # Verifica que se llamó a query

def test_create_user(mock_db):
    repo = UserRepository(mock_db)
    
    # Ejecutamos
    new_user = repo.create("nuevo", "a@a.com", "hash123")

    # Verificamos que se ejecutaron las operaciones de DB
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

import pytest
from src.infrastructure.security.security_repository import SecurityServicesRepo

@pytest.fixture
def security_service():
    return SecurityServicesRepo()

def test_hash_and_verify_password(security_service):
    # Arrange
    password = "mi_password_segura_123"
    
    # Act
    hashed = security_service.hash_password(password)
    
    # Assert
    assert hashed != password  # El hash no debe ser igual al texto plano
    assert security_service.verify_password(password, hashed) is True

def test_verify_password_fails(security_service):
    # Arrange
    password = "password_real"
    hashed = security_service.hash_password(password)
    
    # Act & Assert
    assert security_service.verify_password("password_incorrecta", hashed) is False

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.infrastructure.predictions.ml_repository import PredictionProvider

@pytest.fixture
def provider():
    return PredictionProvider()

# --- TEST GET_CONTRACTS ---

@patch('src.infrastructure.predictions.ml_repository.NLPpreprocessor')
@patch('src.infrastructure.predictions.ml_repository.cosine_similarity')
@patch('src.infrastructure.predictions.ml_repository.dfNLP') # Mockeamos el dataframe global
def test_get_contracts(mock_df, mock_cosine, mock_preprocessor, provider):
    # 1. Configuramos el mock para que el dataframe devuelva algo controlado
    # Simulamos que al hacer sort_values().head(5) devuelve un dict
    mock_df.sort_values.return_value.head.return_value.to_dict.return_value = {"id": 1}
    
    # 2. Ejecutamos
    resultado = provider.get_contracts("descripcion test")
    
    # 3. Verificamos
    assert resultado == {"id": 1}
    mock_preprocessor.transform.assert_called_once()

