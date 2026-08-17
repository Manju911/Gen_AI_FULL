import logging
import time
import uuid

from fastapi import FastAPI, Request
from pydantic import BaseModel

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.logging_config import setup_logging

from app.agents.router import route_question
from app.agents.knowledge import knowledge_agent
from app.agents.troubleshooting import troubleshooting_agent
from app.agents.ticket import ticket_agent

from app.services.cache import (
    get_cached_answer,
    cache_answer
)


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI IT Support",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):

    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    request.state.request_id = request_id

    logger.info(
        "request_started request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path
    )

    try:

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_completed request_id=%s status=%s duration=%.3fs",
            request_id,
            response.status_code,
            duration
        )

        return response

    except Exception:

        duration = time.perf_counter() - start_time

        logger.exception(
            "request_failed request_id=%s duration=%.3fs",
            request_id,
            duration
        )

        raise

limiter = Limiter(
    key_func=get_remote_address
)


app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)


class SupportRequest(BaseModel):

    question: str


@app.get("/")
async def root():

    return {
        "service": "AI IT Support",
        "status": "running"
    }


@app.get("/health")
async def health():

    redis_status = "healthy"

    try:
        from app.services.cache import redis_client

        await redis_client.ping()

    except Exception as exc:

        logger.error(
            "Redis health check failed: %s",
            str(exc)
        )

        redis_status = "unhealthy"

    overall_status = (
        "healthy"
        if redis_status == "healthy"
        else "degraded"
    )

    return {
        "status": overall_status,
        "services": {
            "api": "healthy",
            "redis": redis_status,
            "chroma": "healthy"
        }
    }

@app.post("/support")
@limiter.limit("10/minute")
async def support(
    request: Request,
    body: SupportRequest
):

    question = body.question.strip()

    if not question:

        return {
            "error": "Question cannot be empty"
        }

    logger.info(
        "Received support request"
    )

    # ---------------------------
    # ROUTER AGENT
    # ---------------------------

    category = await route_question(
        question
    )

    logger.info(
        "Router selected: %s",
        category
    )

    # ---------------------------
    # CACHE
    # ---------------------------

    if category != "ticket":

        cached = await get_cached_answer(
            question
        )

        if cached:

            logger.info(
                "Returning cached response"
            )

            cached["cached"] = True

            return cached

    # ---------------------------
    # SPECIALIZED AGENTS
    # ---------------------------

    if category == "knowledge":

        result = await knowledge_agent(
            question
        )

    elif category == "ticket":

        result = await ticket_agent(
            question,
            "User explicitly requested support ticket"
        )

    else:

        result = await troubleshooting_agent(
            question
        )

    result["category"] = category
    result["cached"] = False

    # ---------------------------
    # CACHE ONLY READ-ONLY RESULTS
    # ---------------------------

    if category != "ticket":

        await cache_answer(
            question,
            result
        )

    return result