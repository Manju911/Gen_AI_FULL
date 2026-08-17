import time
import logging

from celery import Celery

from app.core.config import settings


logger = logging.getLogger(__name__)


celery_app = Celery(
    "it_support_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task
def create_ticket(
    question: str,
    reason: str
):

    logger.info(
        "Starting ticket creation"
    )

    # Simulate external ticketing system
    time.sleep(5)

    ticket_id = "IT-" + str(
        int(time.time())
    )

    logger.info(
        "Ticket created: %s",
        ticket_id
    )

    return {
        "ticket_id": ticket_id,
        "status": "created",
        "question": question,
        "reason": reason
    }