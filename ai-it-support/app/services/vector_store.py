import os

import chromadb
from openai import AsyncOpenAI

from app.core.config import settings


CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "./chroma_db"
)


chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_or_create_collection(
    name="it_support"
)


openai_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)


async def create_embedding(text: str):

    response = await openai_client.embeddings.create(
        model=settings.OPENAI_EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


async def add_document(
    document_id: str,
    text: str
):

    embedding = await create_embedding(text)

    collection.upsert(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding]
    )


async def search_documents(
    query: str,
    k: int = 3
):

    embedding = await create_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents