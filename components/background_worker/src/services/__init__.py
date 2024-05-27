from .kafka_consumer import KafkaConsumerUpstreamService
from .mongodb import BeanieMongoDBUpstreamService
from .openai import OpenAIUpstreamService

_service_classes = [
    KafkaConsumerUpstreamService,
    BeanieMongoDBUpstreamService,
    OpenAIUpstreamService
]

_services = {}
for cls in _service_classes:
    _services[cls.NAME] = cls()

def get_all_services():
    return _services
