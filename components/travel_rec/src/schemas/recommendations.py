from pydantic import BaseModel, Field, field_validator

SEASONS = ['spring', 'summer', 'fall', 'winter']

class SearchParams(BaseModel):
    country: str = Field(..., description='Country to visit')
    season: str = Field(..., description='Season')

    @field_validator('season')
    @classmethod
    def validate_season(cls, value: str) -> str:
        season = value.lower()
        if season not in SEASONS:
            raise ValueError('Season is not valid!')
        return season


class GetResultsParams(BaseModel):
    id: str = Field(..., description='Request uuid')
