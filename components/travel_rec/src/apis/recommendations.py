"""
Handle get recommendations request
"""
from fastapi import APIRouter, Depends

from ..controllers.recommendations import process_recommendation, get_results
from ..schemas.recommendations import GetResultsParams, SearchParams

recommendations_router = APIRouter(
    prefix='/v1/recommendations',
    tags=['Recommendations']
)

@recommendations_router.get('/')
async def get_recommendations(params: SearchParams = Depends(SearchParams)):
    return await process_recommendation(
        country=params.country,
        season=params.season
    )

@recommendations_router.get('/results')
async def get_recommendation_results(params: GetResultsParams = Depends(GetResultsParams)):
    return await get_results(rec_id=params.id)
