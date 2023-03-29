from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from starlette import status
from starlette.responses import Response

from schemas.base import OrderEnum
from schemas.statistic import StatisticCreateSchema, StatisticRetrieveSchema
from services.statistic import StatisticService

router = APIRouter()


@router.post("/", response_model=StatisticRetrieveSchema)
async def create_statistic(statistic: StatisticCreateSchema, service: StatisticService = Depends()):
    """Метод сохранения статистики"""
    return await service.create(statistic)


@router.get("/", response_model=list[StatisticRetrieveSchema])
async def get_statistic(
        from_date: date = Query(alias="from", description="Дата начала периода (включительно)"),
        to_date: date = Query(alias="to", description="Дата окончания периода (включительно)"),
        sort: str | None = Query(None,
                                 description="Сортировка по полю",
                                 enum=[f for f in StatisticRetrieveSchema.__fields__]),
        order: OrderEnum = Query(...),
        service: StatisticService = Depends(),
):
    """Метод показа статистики"""
    return await service.get_all(from_date, to_date, sort, order)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic(
        service: StatisticService = Depends()
):
    """Метод сброса статистики"""
    if await service.delete_all():
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404)
