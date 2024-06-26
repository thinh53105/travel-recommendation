import asyncio
import json
import time
import sys

from .config import config
from .exceptions import UpstreamServiceUnavailable
from .logging import logger
from .services import get_all_services
from .services.kafka_consumer import KafkaConsumerUpstreamService
from .services.mongodb import BeanieMongoDBUpstreamService
from .services.openai import OpenAIUpstreamService


async def consume(services: dict):
    db: BeanieMongoDBUpstreamService = services['beanie-mongodb']
    openai: OpenAIUpstreamService = services['openai']
    consumer: KafkaConsumerUpstreamService = services['kafka-consumer']

    try:
        # Consume messages
        async for msg in consumer.consumer:
            logger.info('Consumed message: %s', msg.value)
            message = json.loads(msg.value.decode('utf-8'))
            try:
                recommendations = await openai.get_recommendations(
                    message['country'], message['season']
                )
            except UpstreamServiceUnavailable:
                await db.update_failed_status_by_id(message['uid'])
            else:
                await db.update_recommendations_by_id(message['uid'], recommendations)
    finally:
        pass

async def main():
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
    await consume(services)
    for service in services.values():
        await service.stop()

if __name__ == '__main__':
    logger.info(
        'Sleep %s seconds to wait kafka server completely up.',
        config.START_UP_SLEEP_TIME
    )
    time.sleep(config.START_UP_SLEEP_TIME)
    asyncio.run(main())
