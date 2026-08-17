from app.workers.ticket_worker import create_ticket


async def ticket_agent(
    question: str,
    reason: str
):

    task = create_ticket.delay(
        question,
        reason
    )

    return {
        "agent": "ticket_agent",
        "message": "IT support ticket creation started.",
        "task_id": task.id
    }