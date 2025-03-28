import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import DB_PORT, DB_HOST, DB_NAME, DB_PASS, DB_USER

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(autocommit = False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db_conn():
    db: AsyncSession = SessionLocal()

    try:
        yield db
    finally:
        await db.close()