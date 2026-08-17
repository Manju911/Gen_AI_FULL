from app.services.openai_service import ask_openai


async def troubleshooting_agent(question: str):

    system_prompt = """
You are an IT troubleshooting specialist.

Help users troubleshoot common IT problems.

Give practical steps.

Rules:

1. Start with the safest and simplest solution.
2. Give numbered steps.
3. Do not recommend destructive actions.
4. If administrator access is required, clearly mention it.
5. If the issue cannot be solved safely, recommend
   creating an IT support ticket.
"""

    answer = await ask_openai(
        system_prompt=system_prompt,
        user_prompt=question
    )

    return {
        "agent": "troubleshooting_agent",
        "answer": answer
    }