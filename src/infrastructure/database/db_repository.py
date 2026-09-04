from sqlalchemy.orm import Session

from src.domain.entities import User
from src.domain.interfaces import UserRepositoryInterface, PredictionRepositoryInterface
from src.infrastructure.database.models import PredictionsTable, UsersTable

class PredictionsRepository(PredictionRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db
    def save_prediction_db(self, model_used: str, prediction: str, user_id:int):
        new_prediction = PredictionsTable(
            modelused=model_used,
            prediction=prediction,
            owner_id=user_id)
        self.db.add(new_prediction)
        self.db.commit()
        self.db.refresh(new_prediction)
        return new_prediction
    def get_prediction_db(self, user_id: int):
        predictions = self.db.query(PredictionsTable).filter(PredictionsTable.owner_id == user_id).all()
        if predictions is None:
            return None
        return predictions
    def delete_prediction_db(self, prediction_id: int, owner_id: int):
        prediction = self.db.query(PredictionsTable).filter(PredictionsTable.id == prediction_id, PredictionsTable.owner_id == owner_id).first()
        if prediction is None:
            return None
        self.db.delete(prediction)
        self.db.commit()
        return {"status": "borrado"}
    
class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db
    def get_by_username(self, username: str):
        user = self.db.query(UsersTable).filter(UsersTable.username == username).first()
        if user is None:
            return None
        return user
    def get_by_email(self, email: str):
        user = self.db.query(UsersTable).filter(UsersTable.email == email).first()
        return user
        
    def create(self, username: str, email: str, hashed_password: str):
        new_user = UsersTable(
            username=username,
            email=email,
            hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user