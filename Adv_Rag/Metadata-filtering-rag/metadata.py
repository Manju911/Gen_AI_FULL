# import chromadb
# from sentence_transformers import SentenceTransformer

# # ------------------------------------------------------------
# # Sample Documents
# # ------------------------------------------------------------

# documents = [
#     {
#         "id": "1",
#         "text": "Employees are entitled to 20 paid leaves every year.",
#         "metadata": {
#             "file_name": "HR_Policy.txt",
#             "department": "HR",
#             "year": 2025
#         }
#     },
#     {
#         "id": "2",
#         "text": "Python supports object-oriented programming.",
#         "metadata": {
#             "file_name": "Python_Notes.txt",
#             "department": "Training",
#             "year": 2024
#         }
#     },
#     {
#         "id": "3",
#         "text": "Medical insurance covers hospitalization and surgeries.",
#         "metadata": {
#             "file_name": "Medical_Policy.txt",
#             "department": "Medical",
#             "year": 2025
#         }
#     },
#     {
#         "id": "4",
#         "text": "Sales employees receive quarterly incentives.",
#         "metadata": {
#             "file_name": "Sales_Guide.txt",
#             "department": "Sales",
#             "year": 2025
#         }
#     }
# ]

# # ------------------------------------------------------------
# # Load Embedding Model
# # ------------------------------------------------------------

# model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# texts = [doc["text"] for doc in documents]
# embeddings = model.encode(texts)

# # ------------------------------------------------------------
# # Store in ChromaDB
# # ------------------------------------------------------------

# client = chromadb.Client()

# collection = client.create_collection("company_docs")

# collection.add(
#     ids=[doc["id"] for doc in documents],
#     documents=texts,
#     embeddings=embeddings.tolist(),
#     metadatas=[doc["metadata"] for doc in documents]
# )

# # ============================================================
# # Dynamic Metadata Filtering
# # ============================================================

# user_query = input("Ask your question: ")

# # Build metadata filter dynamically
# metadata_filter = {}

# if "HR" in user_query:
#     metadata_filter["department"] = "HR"

# elif "Medical" in user_query:
#     metadata_filter["department"] = "Medical"

# elif "Sales" in user_query:
#     metadata_filter["department"] = "Sales"

# elif "Python" in user_query:
#     metadata_filter["department"] = "Training"

# # Embed user query
# query_embedding = model.encode(user_query)

# # Search
# if metadata_filter:
#     print("\nMetadata Filter Applied:", metadata_filter)

#     results = collection.query(
#         query_embeddings=[query_embedding.tolist()],
#         where=metadata_filter,
#         n_results=2
#     )
# else:
#     print("\nNo Metadata Filter Applied")

#     results = collection.query(
#         query_embeddings=[query_embedding.tolist()],
#         n_results=2
#     )

# # Display Results
# print("\nRetrieved Documents:\n")

# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"File       : {meta['file_name']}")
#     print(f"Department : {meta['department']}")
#     print(f"Year       : {meta['year']}")
#     print(f"Content    : {doc}")
#     print("-" * 50)


# import os
# from openai import OpenAI
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# # =====================================================
# # OpenAI API Key
# # =====================================================
# client = OpenAI(api_key="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")

# # =====================================================
# # Documents
# # =====================================================

# DOCUMENTS = {
#     "HR": "HR_Policy.txt",
#     "Medical": "Medical_Policy.txt",
#     "Python": "Python_Notes.txt",
#     "Sales": "Sales_Guide.txt"
# }

# # =====================================================
# # User Question
# # =====================================================

# query = input("Enter your question: ")

# # =====================================================
# # Router Prompt
# # =====================================================

# router_prompt = f"""
# You are an intelligent document router for a Retrieval-Augmented Generation (RAG) system.

# Your ONLY job is to identify which ONE document should be searched to answer the user's question.

# ========================
# AVAILABLE DOCUMENTS
# ========================

# Document: HR

# Contains information about:
# - Company HR policies
# - Employee leave policy
# - Casual Leave
# - Sick Leave
# - Earned Leave
# - Leave application process
# - Working hours
# - Employee salary
# - Company festivals
# - Company rules
# - Office timings

# Examples:
# - How many leaves are available?
# - What is the salary?
# - What are the working hours?
# - Is Deepawali a company festival?
# - What is the leave policy?

# ----------------------------------------

# Document: Medical

# Contains information about:
# - Medical insurance
# - Employee health insurance
# - Hospitalization
# - Emergency treatment
# - Surgeries
# - Day-care procedures
# - Annual health checkups
# - Insurance for spouse
# - Insurance for dependent children

# Examples:
# - What medical benefits are provided?
# - Is hospitalization covered?
# - Can I add my spouse?
# - Is health checkup free?

# ----------------------------------------

# Document: Python

# Contains information about:
# - Python programming language
# - Python features
# - Object-Oriented Programming
# - Functional Programming
# - Dynamic Typing
# - Standard Library
# - Data Types
# - int
# - float
# - string
# - list
# - tuple
# - dictionary
# - AI
# - Machine Learning
# - Data Science
# - Automation
# - Web Development

# Examples:
# - What is Python?
# - Explain OOP.
# - What are Python data types?
# - Where is Python used?

# ----------------------------------------

# Document: Sales

# Contains information about:
# - Sales department
# - Quarterly incentives
# - Revenue targets
# - Customer acquisition
# - Customer retention
# - Product upselling
# - Annual bonuses
# - Recognition awards
# - Sales meetings

# Examples:
# - How are incentives calculated?
# - What are the KPIs?
# - When is the sales meeting?
# - How are bonuses given?

# ========================
# ROUTING RULES
# ========================

# 1. Select ONLY ONE document.
# 2. Choose the document that is MOST relevant.
# 3. Even if the question contains similar words, think about the meaning before selecting.
# 4. Never explain your reasoning.
# 5. Return ONLY one of these exact words:

# HR
# Medical
# Python
# Sales

# ========================
# User Question
# ========================

# {query}
# """

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     messages=[
#         {"role": "system", "content": "You are a document routing assistant."},
#         {"role": "user", "content": router_prompt}
#     ],
#     temperature=0
# )

# selected_doc = response.choices[0].message.content.strip()

# print(f"\nSelected Document: {selected_doc}")

# # =====================================================
# # Load only selected document
# # =====================================================

# filename = DOCUMENTS.get(selected_doc)

# if filename is None:
#     print("No matching document found.")
#     exit()

# with open(filename, "r", encoding="utf-8") as f:
#     document = f.read()

# print(f"Loaded File: {filename}")

# # =====================================================
# # Chunking
# # =====================================================

# chunks = [
#     chunk.strip()
#     for chunk in document.split("\n\n")
#     if chunk.strip()
# ]

# # =====================================================
# # Embeddings
# # =====================================================

# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# doc_embeddings = embedding_model.encode(chunks)

# query_embedding = embedding_model.encode([query])

# scores = cosine_similarity(
#     query_embedding,
#     doc_embeddings
# )[0]

# best_index = scores.argmax()
# best_chunk = chunks[best_index]

# print("\nRetrieved Context:\n")
# print(best_chunk)

# # =====================================================
# # Final RAG Answer
# # =====================================================

# answer_prompt = f"""
# Answer the question using ONLY the context below.

# Context:
# {best_chunk}

# Question:
# {query}
# """

# answer = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     messages=[
#         {
#             "role": "system",
#             "content": "Answer only from the given context."
#         },
#         {
#             "role": "user",
#             "content": answer_prompt
#         }
#     ],
#     temperature=0
# )

# print("\nFinal Answer:\n")
# print(answer.choices[0].message.content)



import os
import numpy as np
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# OpenAI
# ======================================================

client = OpenAI(api_key="")


# ======================================================
# Available Documents
# ======================================================

DOCUMENTS = {
    "HR": "HR_Policy.txt",
    "Medical": "Medical_Policy.txt",
    "Python": "Python_Notes.txt",
    "Sales": "Sales_Guide.txt"
}

# ======================================================
# User Question
# ======================================================

query = input("Enter your question: ")

# ======================================================
# Router Prompt
# ======================================================

router_prompt = f"""
You are an intelligent document router.

Your job is ONLY to identify which document should answer the question.

Available Documents

----------------------------------------

HR

Contains:

- Leave Policy
- Casual Leave
- Sick Leave
- Earned Leave
- Salary
- Festivals
- Working Hours
- Attendance
- Employee Rules

----------------------------------------

Medical

Contains:

- Medical Insurance
- Hospitalization
- Emergency Treatment
- Surgery
- Health Checkup
- Spouse Coverage
- Dependent Children

----------------------------------------

Python

Contains:

- Python Programming
- OOP
- Functional Programming
- Data Types
- AI
- Machine Learning
- Automation
- Web Development

----------------------------------------

Sales

Contains:

- Quarterly Incentives
- Revenue
- Customer Acquisition
- Customer Retention
- Bonuses
- Sales Meetings

----------------------------------------

Question:

{query}

Return ONLY one word.

HR
Medical
Python
Sales

Nothing else.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": "You are a routing assistant."
        },
        {
            "role": "user",
            "content": router_prompt
        }
    ]
)

selected_doc = response.choices[0].message.content.strip()

print("\nSelected Document:", selected_doc)

# ======================================================
# Load Selected File
# ======================================================

filename = DOCUMENTS[selected_doc]

with open(filename, encoding="utf-8") as f:
    text = f.read()

print("Loaded File:", filename)

# ======================================================
# Better Chunking
# ======================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

print(f"\nTotal Chunks : {len(chunks)}")

# ======================================================
# Embedding Model
# ======================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

doc_embeddings = embedding_model.encode(chunks)

query_embedding = embedding_model.encode([query])

scores = cosine_similarity(
    query_embedding,
    doc_embeddings
)[0]

# ======================================================
# Top-K Retrieval
# ======================================================

TOP_K = 5

top_indices = np.argsort(scores)[::-1][:TOP_K]

candidate_chunks = [
    chunks[i]
    for i in top_indices
]

print("\nRetrieved Chunks\n")

for i, chunk in enumerate(candidate_chunks, 1):

    print(f"\nChunk {i}\n")
    print(chunk)

# ======================================================
# Reranker
# ======================================================

print("\nReranking...\n")

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)

pairs = [
    [query, chunk]
    for chunk in candidate_chunks
]

rerank_scores = reranker.predict(pairs)

sorted_indices = np.argsort(rerank_scores)[::-1]

reranked_chunks = [
    candidate_chunks[i]
    for i in sorted_indices
]

# ======================================================
# Final Context
# ======================================================

context = "\n\n".join(
    reranked_chunks[:3]
)

print("\nFinal Context\n")
print(context)

# ======================================================
# Final Answer
# ======================================================

answer_prompt = f"""
You are a helpful assistant.

Answer ONLY using the context.

If the answer is not present, say:

"I don't know based on the provided document."

Context

{context}

Question

{query}
"""

answer = client.chat.completions.create(
    model="gpt-4.1-mini",
    temperature=0,
    messages=[
        {
            "role":"system",
            "content":"Answer only from the context."
        },
        {
            "role":"user",
            "content":answer_prompt
        }
    ]
)

print("\n========================")
print("FINAL ANSWER")
print("========================\n")

print(answer.choices[0].message.content)