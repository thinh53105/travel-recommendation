"""
Handle logic for recommendations endpoints
"""
import json

from ..services import get_all_services
from ..services.kafka_producer import KafkaProducerUpstreamService
from ..services.mongodb import BeanieMongoDBUpstreamService


async def process_recommendation(country: str, season: str):
    """
    Process recommendation
    """
    producer: KafkaProducerUpstreamService = get_all_services()['kafka-producer']
    db: BeanieMongoDBUpstreamService = get_all_services()['beanie-mongodb']

    document_id = await db.insert_recommendations_info(country, season, status='pending')

    value_json = {
        'uid': str(document_id),
        'country': country,
        'season': season
    }

    await producer.produce_message(json.dumps(value_json).encode('utf-8'))

    return {'uid': document_id}

async def get_results(rec_id: str):
    """
    Get recommendation result
    """
    db: BeanieMongoDBUpstreamService = get_all_services()['beanie-mongodb']

    result_dict = await db.find_recommendation_by_id(rec_id)
    if result_dict['status'] == 'completed':
        return result_dict

    if result_dict['status'] == 'pending':
        return {
            'uid': result_dict['uid'],
            'status': 'pending',
            'message': 'The recommendations are not yet available. Please try again later.'
        }

    if result_dict['status'] == 'failed':
        return {
            'uid': result_dict['uid'],
            'status': 'failed',
            'reason': result_dict['reason']
        }
