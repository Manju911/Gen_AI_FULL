import hashlib
import json

import redis.asyncio as redis

from app.core.config import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)


def create_cache_key(question: str):

    normalized = question.lower().strip()

    hashed = hashlib.sha256(
        normalized.encode()
    ).hexdigest()

    return f"ai_support:{hashed}"


async def get_cached_answer(
    question: str
):

    key = create_cache_key(question)

    value = await redis_client.get(key)

    if value:
        return json.loads(value)

    return None


async def cache_answer(
    question: str,
    answer: dict
):

    key = create_cache_key(question)

    await redis_client.setex(
        key,
        settings.CACHE_TTL,
        json.dumps(answer)
    )