import pytest
import redis
import fakeredis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.infrastructure.database.models import UsersTable, PredictionsTable
from src.infrastructure.database.connection import Base
from src.infrastructure.cache.cache import CacheServices
from src.infrastructure.celery.celery_app import celery_app
# 1. Configuración de la Base de Datos (PostgreSQL)

@pytest.fixture(scope="session", autouse=True)
def configure_celery_for_tests():
    """Configura Celery para ejecutar tareas en el mismo proceso durante los tests."""
    celery_app.conf.update(
        task_always_eager=True,          # Ejecuta las tareas al instante (sin broker)
        task_eager_propagates=True,      # Propaga errores si la tarea falla
        broker_url="memory://",          # Usa broker en memoria
        result_backend="cache+memory://" # Usa backend en memoria
    )
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,)
    Base.metadata.create_all(engine)
    print(Base.metadata.tables.keys())
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# 2. Configuración de Redis
@pytest.fixture(scope="session")
def redis_client():
    client = fakeredis.FakeRedis()
    # Limpiar Redis antes de empezar los tests
    client = fakeredis.FakeRedis()
    yield client
    client.flushall()
# 3. Cliente de Test (FastAPI/Flask/etc)
@pytest.fixture(scope="module")
def client(db_session, redis_client):
    from src.infrastructure.api.main import app
    from src.infrastructure.api.dependencies import get_cache_service
    from src.infrastructure.database.connection import get_db
    
    cache_service_instance = CacheServices(redis_client=redis_client)
    # Sobrescribir la dependencia de la DB para usar la sesión de test
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_cache_service] = lambda: cache_service_instance
    
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpieza de overrides al terminar
    app.dependency_overrides.clear()