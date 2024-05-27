import time

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .apis.recommendations import recommendations_router
from .config import config
from .exceptions import configure_exception
from .logging import logger
from .services import get_all_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sleep to wait kafka completely up
    logger.info(
        'Sleep %s seconds to wait kafka server completely up.',
        config.START_UP_SLEEP_TIME
    )
    time.sleep(config.START_UP_SLEEP_TIME)
    services = get_all_services()
    for service in services.values():
        await service.start()
    yield
    for service in services.values():
        await service.stop()

app = FastAPI(
    docs_url=config.API_PREFIX,
    lifespan=lifespan
)
app.include_router(recommendations_router, prefix=config.API_PREFIX)

configure_exception(app=app)
