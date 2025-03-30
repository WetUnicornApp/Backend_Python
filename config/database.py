import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# importujemy odpowiednie klasy z SQLAlchemy, aby obsługiwać asynchroniczne operacje na bazie danych
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

#Tworzenie sesji
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
