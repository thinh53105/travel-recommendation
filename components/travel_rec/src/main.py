import time
import sys

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
    retries = config.START_UP_RETRIES
    for service in services.values():
        for i in range(retries):
            try:
                await service.start()
                break
            except Exception:
                if i != retries - 1:
                    logger.error('Service `%s` fail to start. Retry...', service.NAME)
                    time.sleep(config.RETRY_SLEEP_TIME)
                else:
                    logger.error('Service `%s` fail to start. Exit...', service.NAME)
                    sys.exit(1)
    yield
    for service in services.values():
        await service.stop()

if __name__ == '__main__':
    app = FastAPI(
        docs_url=f'{config.API_PREFIX}/docs',
        lifespan=lifespan
    )
    app.include_router(recommendations_router, prefix=config.API_PREFIX)

    configure_exception(app=app)
