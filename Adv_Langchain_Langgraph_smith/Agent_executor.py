from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------------------------
# Tool 1
# --------------------------------------------------
@tool
def calculator(number: int) -> str:
    """Use this tool to calculate the square of a number."""
    return f"Square of {number} is {number * number}"


# --------------------------------------------------
# Tool 2
# --------------------------------------------------
@tool
def weather(city: str) -> str:
    """Use this tool to get the current weather of a city."""
    weather_data = {
        "bangalore": "28°C, Cloudy",
        "mumbai": "31°C, Sunny",
        "delhi": "38°C, Hot"
    }

    return weather_data.get(city.lower(), "Weather not available")


# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=0
)

tools = [calculator, weather]

# --------------------------------------------------
# Prompt
# --------------------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

# --------------------------------------------------
# Create Agent
# --------------------------------------------------
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# --------------------------------------------------
# Agent Executor
# --------------------------------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# --------------------------------------------------
# User Input
# --------------------------------------------------
question = input("Ask your question: ")

response = agent_executor.invoke(
    {
        "input": question
    }
)

print("\nFinal Answer:")
print(response["output"])