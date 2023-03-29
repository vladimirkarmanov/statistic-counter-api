from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from pydantic.fields import Field


class StatisticCreateSchema(BaseModel):
    date: date
    views: int | None = Field(..., ge=0)
    clicks: int | None = Field(..., ge=0)
    cost: Decimal | None = Field(..., ge=0.0, max_digits=7, decimal_places=2)


class StatisticRetrieveSchema(StatisticCreateSchema):
    cpc: Decimal | None  # (средняя стоимость клика)
    cpm: Decimal | None  # (средняя стоимость 1000 показов)

    class Config:
        orm_mode = True
