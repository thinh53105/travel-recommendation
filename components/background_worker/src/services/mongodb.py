from typing import Optional, List
from uuid import uuid4

from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from pymongo.errors import PyMongoError

from ..config import config
from ..logging import logger
from ..exceptions import RecordNotExists, UpstreamServiceUnavailable


class RecommendationsDocument(Document):
    uid: str = Field(default_factory=lambda: str(uuid4()))
    country: str
    season: str
    status: str
    reason: Optional[str] = Field(default_factory=lambda: '')
    recommendations: Optional[List] = Field(default_factory=lambda: [])

    class Settings:
        collection = 'recommendations'


class BeanieMongoDBUpstreamService:
    NAME = 'beanie-mongodb'

    def __init__(self) -> None:
        self._client = AsyncIOMotorClient(config.mongo_db.MONGODB_URI)

    async def start(self):
        await init_beanie(
            database=self._client.db_name,
            document_models=[RecommendationsDocument]
        )
        logger.info('Service `%s` started.', self.NAME)

    async def stop(self):
        if self._client:
            self._client.close()
        logger.info('Service `%s` stopped.', self.NAME)

    async def update_recommendations_by_id(self, document_id: str, recommendations: list):
        try:
            document = await RecommendationsDocument.find_one(
                RecommendationsDocument.uid == document_id
            )
            if document is None:
                logger.error('Record with id=%s not exists', document_id)
                raise RecordNotExists()

            status = 'completed'
            await document.set({
                RecommendationsDocument.status: status,
                RecommendationsDocument.recommendations: recommendations
            })
            logger.info(
                'Updated record with id=%s value %s',
                document_id,
                {'status': status, 'recommendations': recommendations}
            )
        except PyMongoError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)

    async def update_failed_status_by_id(self, document_id):
        try:
            document = await RecommendationsDocument.find_one(
                RecommendationsDocument.uid == document_id
            )
            if document is None:
                logger.error('Record with id=%s not exists', document_id)
                raise RecordNotExists()

            status, reason = 'failed', 'Upstream Service Unavailable'
            await document.set({
                RecommendationsDocument.status: status,
                RecommendationsDocument.reason: reason
            })
            logger.info(
                'Updated record with id=%s value %s',
                document_id,
                {'status': status, 'reason': reason}
            )
        except PyMongoError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)
