import asyncio
from config.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def test_connection():
    try:
        async with AsyncSession(engine) as session:
            result = await session.execute(select(1))
            print(f" Połączenie z bazą danych działa! Wynik zapytania: {result.scalar()}")
    except Exception as e:
        print(f" Błąd połączenia: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())

