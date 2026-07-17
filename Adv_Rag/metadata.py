import chromadb
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------
# Sample Documents
# ------------------------------------------------------------

documents = [
    {
        "id": "1",
        "text": "Employees are entitled to 20 paid leaves every year.",
        "metadata": {
            "file_name": "HR_Policy.txt",
            "department": "HR",
            "year": 2025
        }
    },
    {
        "id": "2",
        "text": "Python supports object-oriented programming.",
        "metadata": {
            "file_name": "Python_Notes.txt",
            "department": "Training",
            "year": 2024
        }
    },
    {
        "id": "3",
        "text": "Medical insurance covers hospitalization and surgeries.",
        "metadata": {
            "file_name": "Medical_Policy.txt",
            "department": "Medical",
            "year": 2025
        }
    },
    {
        "id": "4",
        "text": "Sales employees receive quarterly incentives.",
        "metadata": {
            "file_name": "Sales_Guide.txt",
            "department": "Sales",
            "year": 2025
        }
    }
]

# ------------------------------------------------------------
# Load Embedding Model
# ------------------------------------------------------------

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

texts = [doc["text"] for doc in documents]
embeddings = model.encode(texts)

# ------------------------------------------------------------
# Store in ChromaDB
# ------------------------------------------------------------

client = chromadb.Client()

collection = client.create_collection("company_docs")

collection.add(
    ids=[doc["id"] for doc in documents],
    documents=texts,
    embeddings=embeddings.tolist(),
    metadatas=[doc["metadata"] for doc in documents]
)

# ============================================================
# Dynamic Metadata Filtering
# ============================================================

user_query = input("Ask your question: ")

# Build metadata filter dynamically
metadata_filter = {}

if "HR" in user_query:
    metadata_filter["department"] = "HR"

elif "Medical" in user_query:
    metadata_filter["department"] = "Medical"

elif "Sales" in user_query:
    metadata_filter["department"] = "Sales"

elif "Python" in user_query:
    metadata_filter["department"] = "Training"

# Embed user query
query_embedding = model.encode(user_query)

# Search
if metadata_filter:
    print("\nMetadata Filter Applied:", metadata_filter)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        where=metadata_filter,
        n_results=2
    )
else:
    print("\nNo Metadata Filter Applied")

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

# Display Results
print("\nRetrieved Documents:\n")

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"File       : {meta['file_name']}")
    print(f"Department : {meta['department']}")
    print(f"Year       : {meta['year']}")
    print(f"Content    : {doc}")
    print("-" * 50)