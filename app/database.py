import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Use an async connection string for PostgreSQL (requires the asyncpg driver)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg:///admin_user:administrator@localhost:5432/misconception_db")

# 1. Create the engine (equivalent to a Java DataSource config)
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. Create the Session Factory (equivalent to Hibernate's SessionFactory)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. Create the modern Base Class (replaces declarative_base())
class Base(DeclarativeBase):
    pass

# 4. FastAPI Dependency to provide database sessions to endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
