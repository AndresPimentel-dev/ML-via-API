import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

RAWDBURL = os.getenv("DBURL")

if RAWDBURL and RAWDBURL.startswith("postgres://"):
    DBURL = RAWDBURL.replace("postgres://", "postgresql+psycopg2://", 1)
else:
    DBURL = RAWDBURL or "sqlite:///./local_fallback.db"

engine = create_engine(DBURL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()