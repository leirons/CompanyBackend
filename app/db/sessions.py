from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:leirons3004@localhost/postgres"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,echo=True
# )


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Get db to create session
    :return Session:
    """
    async with session_local() as session:
        yield session
