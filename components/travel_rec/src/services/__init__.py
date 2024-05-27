from .kafka_producer import KafkaProducerUpstreamService
from .mongodb import BeanieMongoDBUpstreamService

_service_classes = [
    KafkaProducerUpstreamService,
    BeanieMongoDBUpstreamService
]

_services = {}
for cls in _service_classes:
    _services[cls.NAME] = cls()

def get_all_services():
    return _services
