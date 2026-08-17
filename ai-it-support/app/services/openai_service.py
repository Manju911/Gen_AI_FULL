import asyncio
import logging

from openai import AsyncOpenAI

from app.core.config import settings


logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=30.0,
    max_retries=0
)


async def ask_openai(
    system_prompt: str,
    user_prompt: str
) -> str:

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            logger.info(
                "OpenAI request attempt=%s",
                attempt
            )

            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as exc:

            logger.warning(
                "OpenAI request failed attempt=%s error=%s",
                attempt,
                str(exc)
            )

            if attempt == max_attempts:
                logger.error(
                    "OpenAI request failed permanently"
                )
                raise

            await asyncio.sleep(
                2 ** (attempt - 1)
            )