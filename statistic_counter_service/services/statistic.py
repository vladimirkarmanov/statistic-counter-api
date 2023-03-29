from datetime import date

from models.statistic import Statistic
from repositories.statistic import StatisticRepository
from schemas.base import OrderEnum
from schemas.statistic import StatisticCreateSchema, StatisticRetrieveSchema
from services.base import StatisticServiceMixin


class StatisticService(StatisticServiceMixin):
    @property
    def repository(self) -> StatisticRepository:
        return self.statistic_repository

    async def create(self, statistic: StatisticCreateSchema) -> StatisticRetrieveSchema:
        statistic = await self.repository.create(Statistic(**statistic.dict()))
        return StatisticRetrieveSchema.from_orm(statistic)

    async def get_all(
            self,
            from_date: date,
            to_date: date,
            sort: str | None,
            order: OrderEnum,
    ) -> list[StatisticRetrieveSchema]:
        statistics = await self.repository.get_all(from_date, to_date, sort, order)
        return [StatisticRetrieveSchema.from_orm(s) for s in statistics]

    async def delete_all(self) -> bool:
        return await self.repository.delete_all()
