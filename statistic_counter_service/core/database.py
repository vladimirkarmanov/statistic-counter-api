from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from core.settings import Settings

settings = Settings()


def create_engines(settings: Settings) -> tuple[Engine, AsyncEngine]:
    sync_engine: Engine = create_engine(
        settings.DATABASE_URL.replace("+asyncpg", ""),
        max_overflow=settings.DB_ENGINE_MAX_OVERFLOW,
        pool_pre_ping=settings.DB_ENGINE_POOL_PRE_PING,
        pool_recycle=settings.DB_ENGINE_POOL_RECYCLE,
        pool_size=settings.DB_ENGINE_POOL_SIZE,
        pool_timeout=settings.DB_ENGINE_POOL_TIMEOUT,
        echo=settings.SQL_ENGINE_ECHO,
    )
    async_engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        max_overflow=settings.DB_ENGINE_MAX_OVERFLOW,
        pool_pre_ping=settings.DB_ENGINE_POOL_PRE_PING,
        pool_recycle=settings.DB_ENGINE_POOL_RECYCLE,
        pool_size=settings.DB_ENGINE_POOL_SIZE,
        pool_timeout=settings.DB_ENGINE_POOL_TIMEOUT,
        echo=settings.SQL_ENGINE_ECHO,
    )
    return sync_engine, async_engine


def create_sessions(
        engine: Engine, async_engine: AsyncEngine
) -> tuple[Callable[[], Session], Callable[[], AsyncSession]]:
    create_async_session: Callable[[], AsyncSession] = async_sessionmaker(
        bind=async_engine, expire_on_commit=False
    )
    create_session: Callable[[], Session] = sessionmaker(bind=engine, expire_on_commit=False)
    return create_session, create_async_session


engine, async_engine = create_engines(settings)
create_session, create_async_session = create_sessions(engine, async_engine)
