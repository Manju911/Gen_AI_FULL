import os
import shutil
import sqlite3

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# =====================================================
# Load Environment
# =====================================================

load_dotenv()

# =====================================================
# Remove Existing Vector DB
# =====================================================

if os.path.exists("chroma_db"):
    shutil.rmtree("chroma_db")
    print("Old Chroma DB deleted.")

documents = []

# =====================================================
# 1. PDF
# =====================================================

print("\nLoading PDF...")

try:
    pdf_loader = PyPDFLoader("data/company_policy.pdf")
    pdf_docs = pdf_loader.load()

    for doc in pdf_docs:
        doc.metadata["source"] = "pdf"

    documents.extend(pdf_docs)

    print(f"Loaded {len(pdf_docs)} PDF pages.")

except Exception as e:
    print("PDF Error:", e)

# =====================================================
# 2. CSV
# =====================================================

print("\nLoading CSV...")

try:

    df = pd.read_csv("data/employees.csv")

    for _, row in df.iterrows():

        text = f"""
Employee ID : {row['EmployeeID']}
Name : {row['Name']}
Department : {row['Department']}
Role : {row['Role']}
Age : {row['Age']}
Gender : {row['Gender']}
Experience : {row['Experience']}
Salary : {row['Salary']}
Location : {row['Location']}
Manager : {row['Manager']}
Joining Date : {row['JoiningDate']}
Email : {row['Email']}
Phone : {row['Phone']}
Performance Rating : {row['PerformanceRating']}
Project : {row['Project']}
Employment Type : {row['EmploymentType']}
Skills : {row['Skills']}
"""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": "csv",
                    "employee": row["Name"],
                    "department": row["Department"],
                    "location": row["Location"]
                }
            )
        )

    print(f"Loaded {len(df)} CSV records.")

except Exception as e:
    print("CSV Error:", e)

# =====================================================
# 3. SQLite
# =====================================================

print("\nLoading SQLite Database...")
db_path = "data/hospital.db"

print("\n========== SQLITE DEBUG ==========")
print("Current Directory :", os.getcwd())
print("Database Path     :", os.path.abspath(db_path))
print("Exists            :", os.path.exists(db_path))
print("Size              :", os.path.getsize(db_path))
print("==================================")


try:

    conn = sqlite3.connect("data/hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)
    #[(employee
    #dept
    #project)]

    result = cursor.fetchall()
    print(result)
    tables = [row[0] for row in result]
    

    print("Tables Found:", tables)

    for table in tables:

        cursor.execute(f"SELECT * FROM {table}")

        columns = [col[0] for col in cursor.description]

        rows = cursor.fetchall()

        print(f"Loading {table} ({len(rows)} rows)")

        for row in rows:

            text = "\n".join(
                f"{column}: {value}"
                for column, value in zip(columns, row)
            )

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "sqlite",
                        "table": table
                    }
                )
            )

    conn.close()

except Exception as e:
    print("SQLite Error:", e)

# =====================================================
# 4. HTML
# =====================================================

print("\nLoading HTML...")

try:

    with open("data/website.html", "r", encoding="utf8") as f:

        soup = BeautifulSoup(f.read(), "html.parser")

    text = soup.get_text(separator="\n")

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": "html"
            }
        )
    )

    print("HTML Loaded.")

except Exception as e:
    print("HTML Error:", e)

# =====================================================
# Statistics
# =====================================================

print("\n===================================")
print("Total Documents :", len(documents))
print("===================================")

# =====================================================
# Chunking
# =====================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"\nTotal Chunks : {len(chunks)}")

# =====================================================
# Debug - Show Sample Chunks
# =====================================================

print("\n===================================")
print("Sample Chunks")
print("===================================")

for i, chunk in enumerate(chunks[:5]):

    print(f"\nChunk {i+1}")

    print(chunk.metadata)

    print(chunk.page_content[:500])

    print("-" * 60)

# =====================================================
# Embeddings
# =====================================================

print("\nGenerating Embeddings...")

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=""
)

# =====================================================
# Store in Chroma
# =====================================================

print("\nCreating Chroma Vector Database...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="chroma_db"
)

print("\n===================================")
print("Vector DB Created Successfully")
print("===================================")