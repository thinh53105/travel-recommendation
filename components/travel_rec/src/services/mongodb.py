from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from ..config import config
from ..exceptions import RecordNotExists, UpstreamServiceUnavailable
from ..logging import logger
from ..schemas.database import RecommendationsDocument


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

    async def insert_recommendations_info(self, country: str, season: str, status: str):
        try:
            document_object = RecommendationsDocument(
                country=country,
                season=season,
                status=status
            )
            await document_object.insert()
            logger.info(
                'Successfully insert document %s to database.',
                document_object.model_dump()
            )
            document_id = document_object.uid
            return document_id

        except PyMongoError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)

    async def find_recommendation_by_id(self, document_id: str):
        try:
            result = await RecommendationsDocument.find_one(
                RecommendationsDocument.uid == document_id
            )
            if result is None:
                logger.info('Document with id=%s not found.', document_id)
                raise RecordNotExists()

        except PyMongoError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)

        return result.dict()
