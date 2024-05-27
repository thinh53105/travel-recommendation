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


class KafkaConsumerConfig(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = 'kafka:29092'
    KAFKA_TOPIC: str = 'recommendations'


class MongoDBConfig(BaseSettings):
    MONGODB_URI: str = 'mongodb://mongo:27017/recommendations'
    MONGODB_DATABASE: str = 'recommendations'


class OpenAIConfig(BaseSettings):
    OPENAI_API_KEY: str = 'mock_key'
    OPENAI_MODEL: str = 'gpt-3.5-turbo'


class Config(BaseSettings):
    START_UP_SLEEP_TIME: int = 10

    kafka_consumer: KafkaConsumerConfig = KafkaConsumerConfig()
    mongo_db: MongoDBConfig = MongoDBConfig()
    openai: OpenAIConfig = OpenAIConfig()
    logging: LogConfig = LogConfig()

config = Config()
