import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.utils.settings import settings

from app.server import app
from app.db.sessions import Base, get_db

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:leirons3004@localhost:5432/postgres"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def override_get_db() -> AsyncSession:
    """
    Get db to create session
    :return Session:
    """
    async with session_local() as session:
        yield session


@pytest_asyncio.fixture
async def get_session(event_loop) -> AsyncSession:
    async with session_local() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
            app=app,
            base_url="http://testserver/",
            headers={"Content-Type": "application/json"},
    ) as client:
        await start_db()
        yield client
        await engine.dispose()
