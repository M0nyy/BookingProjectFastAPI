from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.settings import settings

if settings.MODE == 'TEST':
    DB_URL: str = f'postgresql+asyncpg://{settings.TESTDB_USER}:{settings.TESTDB_USERPASS}@{settings.TESTDB_HOST}:{settings.TESTDB_PORT}/{settings.TESTDB_NAME}'
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DB_URL: str = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_USERPASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DB_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


class Base(DeclarativeBase):
    pass
