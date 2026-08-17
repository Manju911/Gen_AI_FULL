import json

from app.services.openai_service import ask_openai


async def route_question(question: str):

    system_prompt = """
You are an IT support routing agent.

Classify the user's request into exactly one category.

Possible categories:

1. troubleshooting
2. knowledge
3. ticket

Use these rules:

troubleshooting:
The user has an IT problem and wants steps to fix it.

knowledge:
The user is asking about an IT policy, procedure,
or factual information.

ticket:
The user explicitly wants to raise/create/escalate
a support ticket.

Return ONLY valid JSON:

{
    "category": "troubleshooting"
}
"""

    result = await ask_openai(
        system_prompt=system_prompt,
        user_prompt=question
    )

    try:

        data = json.loads(result)

        category = data.get(
            "category",
            "troubleshooting"
        )

    except Exception:

        category = "troubleshooting"

    return category