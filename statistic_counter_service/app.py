from logging import getLogger
import traceback

from fastapi import FastAPI
from fastapi import Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.api_v1 import api
from core.settings import Settings

settings = Settings()
logger = getLogger('api')

app = FastAPI(
    title="Statistic API",
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(exc)
        data = {
            "message": exc.args[0],
            "cause": {
                "error": str(exc.__class__.__name__),
                "method": request.method,
                "url": str(request.url),
            },
        }
        if settings.SHOW_TRACEBACK:
            data["traceback"] = traceback.format_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=data)


app.middleware('http')(catch_exceptions_middleware)

app.include_router(api.router, prefix="/api/v1")
