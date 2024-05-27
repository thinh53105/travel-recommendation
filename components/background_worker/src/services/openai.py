import asyncio

from openai import AsyncOpenAI, OpenAIError

from ..config import config
from ..exceptions import UpstreamServiceUnavailable
from ..logging import logger


class OpenAIUpstreamService:
    NAME = 'openai'

    def __init__(self) -> None:
        self.key = config.openai.OPENAI_API_KEY
        self._client = AsyncOpenAI(api_key=self.key)
        self.model = config.openai.OPENAI_MODEL

    async def start(self):
        logger.info('Service `%s` started.', self.NAME)

    async def stop(self):
        logger.info('Service `%s` stopped.', self.NAME)

    def create_mock_answer(self):
        return [
            'Go skiing in Whistler.',
            'Experience the Northern Lights in Yukon.',
            'Visit the Quebec Winter Carnival.'
        ]

    def process_content(self, content: str) -> list:
        lines = content.strip().split('\n')
        activities = []
        for line in lines:
            if line[:2] in ['1.', '2.', '3.']:
                activity = line[2:].split(':')[0].strip().split('.')[0].strip() + '.'
                activities.append(activity)
        return activities

    async def get_recommendations(self, country: str, season: str):
        if self.key == 'mock_key':
            await asyncio.sleep(10)
            logger.debug('Return mock answer.')
            return self.create_mock_answer()

        try:
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'user', 'content': f'Recommend me three things to do in {country} during {season}.'}
                ]
            )
            content = response.choices[0].message.content
            logger.debug('Raw content from OpenAI API: %s', content)
            recommendations = self.process_content(content)
            logger.debug('Content processed: %s', recommendations)

        except OpenAIError as ex:
            logger.exception(type(ex).__name__, exc_info=ex)
            raise UpstreamServiceUnavailable(name=self.NAME)

        return recommendations
