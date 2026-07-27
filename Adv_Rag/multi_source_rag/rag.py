
from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# ---------------------------------------
# OpenAI
# ---------------------------------------
API_KEY = ""

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=API_KEY
)

llm = ChatOpenAI(
    model="gpt-5.5",
    api_key=API_KEY,
    temperature=0
)

# ---------------------------------------
# Chroma
# ---------------------------------------
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = db.as_retriever(
    search_kwargs={"k": 10}
)

# ---------------------------------------
# Chat Loop
# ---------------------------------------
while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    print("\nRetrieved Documents")
    print("=" * 80)

    context = []

    for i, doc in enumerate(docs, 1):
        print(f"\nDocument {i}")
        print("Metadata :", doc.metadata)
        print("Content")
        print("-" * 60)
        print(doc.page_content)

        context.append(doc.page_content)

    context = "\n\n".join(context)

    prompt = f"""
You are an Enterprise HR Assistant.

Rules:

1. Answer ONLY from the provided context.
2. Never use outside knowledge.
3. Never guess or infer missing employees.
4. If the retrieved context is insufficient, reply exactly:

I could not find this information in the provided documents.

5. For questions like:
   - highest salary
   - lowest salary
   - list all employees
   - count employees
   - average salary

Only answer if ALL required employee records are present in the context.
Otherwise reply:

I could not find this information in the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    print("\nAnswer")
    print("=" * 80)
    print(response.content)