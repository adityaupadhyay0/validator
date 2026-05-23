from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from aegis_val.api.core.config import settings
from typing import AsyncGenerator

engine = create_async_engine(settings.async_database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
