from app.services.vector_store import search_documents
from app.services.openai_service import ask_openai


async def knowledge_agent(question: str):

    documents = await search_documents(
        question,
        k=3
    )

    context = "\n\n".join(documents)

    prompt = f"""
You are an IT knowledge base agent.

Answer the user's IT support question using
the provided company knowledge base.

If the information is not available,
say that the knowledge base does not contain
enough information.

Knowledge Base:

{context}

User Question:

{question}
"""

    answer = await ask_openai(
        system_prompt=prompt,
        user_prompt=question
    )

    return {
        "agent": "knowledge_agent",
        "answer": answer,
        "sources": documents
    }