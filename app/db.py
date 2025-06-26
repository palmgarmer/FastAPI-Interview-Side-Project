from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

# Database URLs
DATABASE_URL = "sqlite+aiosqlite:///./candidates.db"
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_candidates.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for FastAPI endpoints
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables for production
async def create_tables():
    from app.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Create tables for testing
async def create_test_tables():
    from app.models import Base
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
