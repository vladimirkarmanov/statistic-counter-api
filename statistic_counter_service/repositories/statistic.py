from datetime import date

from sqlalchemy import select, delete

from models.statistic import Statistic
from repositories.base import BaseRepository
from schemas.base import OrderEnum


class StatisticRepository(BaseRepository[Statistic]):
    async def create(self, statistic: Statistic) -> Statistic:
        return await self.save(statistic)

    async def get_all(
            self,
            from_date: date,
            to_date: date,
            sort: str | None,
            order: OrderEnum,
    ) -> list[Statistic] | None:
        statement = (
            select(Statistic)
            .filter(Statistic.date.between(from_date, to_date))
        )
        if sort:
            attr = getattr(Statistic, sort)
            statement = statement.order_by(attr.asc() if order == OrderEnum.ASC else attr.desc())
        else:
            statement = statement.order_by(Statistic.date.asc() if order == OrderEnum.ASC else Statistic.date.desc())

        return await self.all(statement)

    async def delete_all(self) -> bool:
        statement = delete(Statistic)
        result = await self.execute(statement)
        return result.rowcount > 0
