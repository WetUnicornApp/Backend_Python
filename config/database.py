import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

load_dotenv()  # wczyta plik .env

DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()
assert DATABASE_URL, "Brak DATABASE_URL w środowisku"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
