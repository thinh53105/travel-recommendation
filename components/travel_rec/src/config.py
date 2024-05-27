from pydantic_settings import BaseSettings


class LogConfig(BaseSettings):

    LOGGER_NAME: str = 'travel-rec-log'
    LOG_FORMAT: str = '%(levelprefix)s %(message)s'
    LOG_LEVEL: str = 'INFO'

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers: dict = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },

    }
    loggers: dict = {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }


class KafkaProducerConfig(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = 'kafka:29092'
    KAFKA_TOPIC: str = 'recommendations'


class MongoDBConfig(BaseSettings):
    MONGODB_URI: str = 'mongodb://mongo:27017/recommendations'
    MONGODB_DATABASE: str = 'recommendations'


class Config(BaseSettings):
    APP_NAME: str = 'Travel Recommendations API'
    DESCRIPTION: str = 'API for getting recommendations place to travel in a country with specific season'
    API_PREFIX: str = '/api'

    START_UP_SLEEP_TIME: int = 8
    START_UP_RETRIES: int = 3
    RETRY_SLEEP_TIME: int = 3

    kafka_producer: KafkaProducerConfig = KafkaProducerConfig()
    mongo_db: MongoDBConfig = MongoDBConfig()
    logging: LogConfig = LogConfig()

config = Config()
