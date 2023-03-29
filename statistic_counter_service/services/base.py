from logging import Logger

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from api.api_v1.deps import get_settings, get_logger
from core.settings import Settings
from repositories.statistic import StatisticRepository


class BaseService:
    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            logger: Logger = Depends(get_logger),
            settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.logger = logger
        self.settings = settings


class StatisticServiceMixin(BaseService):
    _statistic_repository = None

    @property
    def statistic_repository(self) -> StatisticRepository:
        self._statistic_repository = self._statistic_repository or StatisticRepository(session=self.session)
        return self._statistic_repository
