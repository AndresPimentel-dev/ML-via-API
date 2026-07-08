from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.infrastructure.database.connection import Base

class UsersTable(Base):
    __tablename__ = "UsersTable"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    Predictions: Mapped[List["PredictionsTable"]] = relationship(back_populates="owner")

class PredictionsTable(Base):
    __tablename__ = "PredictionsTable"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    modelused: Mapped[str] = mapped_column(String)
    prediction: Mapped[str] = mapped_column(String)

    owner_id: Mapped[int] = mapped_column(ForeignKey("UsersTable.id"))
    owner: Mapped["UsersTable"] = relationship(back_populates="Predictions")