import logging
import uuid
from asyncio import shield
from logging import Logger
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import create_async_session
from core.settings import Settings

settings = Settings()


def get_logger() -> Logger:
    return logging.getLogger("api")


def get_settings() -> Settings:
    return settings


async def get_session(logger: Logger = Depends(get_logger)) -> AsyncGenerator[AsyncSession, None]:
    session = create_async_session()
    xid = uuid.uuid4()
    try:
        logger.debug(f"[{xid}] Transaction BEGIN;")
        yield session
        await session.commit()
        logger.debug(f"[{xid}] Transaction COMMIT;")
    except DBAPIError as e:
        await session.rollback()
        logger.error(f"[{xid}] Transaction ROLLBACK; (Database Error)")
        raise e
    except Exception:
        await session.rollback()
        logger.error(f"[{xid}] Transaction ROLLBACK; (Application Error)")
        raise
    finally:
        if session:
            await shield(session.close())
            logger.debug(f"[{xid}] Connection released to pool")
