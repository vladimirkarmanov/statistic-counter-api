from fastapi import APIRouter

from api.api_v1.endpoints.statistic import router as statistic_router

router = APIRouter()

router.include_router(statistic_router, prefix="/statistic", tags=["statistic"])
