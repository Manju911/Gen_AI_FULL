


import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

# Load environment variables
load_dotenv()

print("Tracing:", os.getenv("LANGSMITH_TRACING"))
print("Project:", os.getenv("LANGSMITH_PROJECT"))
print("API Key Exists:", bool(os.getenv("LANGSMITH_API_KEY")))

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ------------------- Tools -------------------

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))


@tool
def word_count(text: str) -> str:
    """Count the number of words."""
    return str(len(text.split()))


tools = [calculator, word_count]

# ------------------- Prompt -------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# ------------------- Agent -------------------

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# ------------------- Run -------------------

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    response = executor.invoke({"input": question})

    print("\nAgent:", response["output"])