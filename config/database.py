import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()  # wczyta plik .env

DATABASE_URL = os.getenv("DATABASE_URL")

assert DATABASE_URL, "Brak DATABASE_URL w środowisku"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
