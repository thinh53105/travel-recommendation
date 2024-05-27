from typing import Optional, List
from uuid import uuid4

from beanie import Document
from pydantic import Field


class RecommendationsDocument(Document):
    uid: str = Field(default_factory=lambda: str(uuid4()))
    country: str
    season: str
    status: str
    reason: Optional[str] = Field(default_factory=lambda: '')
    recommendations: Optional[List] = Field(default_factory=lambda: [])

    class Settings:
        collection = 'recommendations'
