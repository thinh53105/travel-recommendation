from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from ..config import config
from ..exceptions import UpstreamServiceUnavailable
from ..logging import logger


class KafkaProducerUpstreamService:
    NAME = 'kafka-producer'

    def __init__(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=config.kafka_producer.KAFKA_BOOTSTRAP_SERVERS
        )
        self.topic = config.kafka_producer.KAFKA_TOPIC


    async def start(self):
        await self._producer.start()
        logger.info('Service `%s` started.', self.NAME)

    async def produce_message(self, message: bytes) -> None:
        try:
            logger.info('Send message %s to topic %s', message, self.topic)
            await self._producer.send_and_wait(self.topic, message)
        except KafkaError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)

    async def stop(self):
        await self._producer.stop()
        logger.info('Service `%s` stopped.', self.NAME)
