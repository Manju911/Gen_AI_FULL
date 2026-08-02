from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

# ---------------------------------------
# LLM
# ---------------------------------------
llm = ChatOpenAI(
    model="gpt-5.5",
    api_key="",
    temperature=0
)

parser = StrOutputParser()

# ---------------------------------------
# Branch 1 - Weather
# ---------------------------------------
weather_chain = (
    ChatPromptTemplate.from_template(
        "You are a weather expert. Answer:\n{question}"
    )
    | llm
    | parser
)

# ---------------------------------------
# Branch 2 - Math
# ---------------------------------------
math_chain = (
    ChatPromptTemplate.from_template(
        "You are a mathematics expert. Solve:\n{question}"
    )
    | llm
    | parser
)

# ---------------------------------------
# Default Branch
# ---------------------------------------
general_chain = (
    ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer:\n{question}"
    )
    | llm
    | parser
)

# ---------------------------------------
# Branching Logic
# ---------------------------------------
branch = RunnableBranch(
    (
        lambda x: "weather" in x["question"].lower(),
        weather_chain,
    ),
    (
        lambda x: any(word in x["question"].lower() for word in ["square", "add", "multiply"]),
        math_chain,
    ),
    general_chain
)

# ---------------------------------------
# User Input
# ---------------------------------------
question = input("Ask your question: ")

response = branch.invoke(
    {
        "question": question
    }
)

print("\nAnswer:")
print(response)