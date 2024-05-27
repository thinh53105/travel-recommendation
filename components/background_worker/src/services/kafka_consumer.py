from aiokafka import AIOKafkaConsumer

from ..config import config
from ..logging import logger


class KafkaConsumerUpstreamService:
    NAME = 'kafka-consumer'

    def __init__(self) -> None:
        self.topic = config.kafka_consumer.KAFKA_TOPIC
        self._consumer = None

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=config.kafka_consumer.KAFKA_BOOTSTRAP_SERVERS,
        )
        await self._consumer.start()
        logger.info('Service `%s` started.', self.NAME)

    @property
    def consumer(self):
        return self._consumer

    async def stop(self):
        await self._consumer.stop()
        logger.info('Service `%s` stopped.', self.NAME)
