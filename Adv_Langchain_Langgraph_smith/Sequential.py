from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# -------------------------------------------------------
# Tool 1
# -------------------------------------------------------
@tool
def calculator(number: int) -> str:
    """
    Calculate the square of a given number.

    Use this tool whenever the user asks about
    squares or square calculations.
    """
    return f"The square of {number} is {number * number}"


# -------------------------------------------------------
# Tool 2
# -------------------------------------------------------
@tool
def weather(city: str) -> str:
    """
    Get the current weather of a city.

    Use this tool whenever the user asks
    about weather, temperature or climate.
    """
    weather_data = {
        "bangalore": "28°C, Cloudy",
        "mumbai": "31°C, Sunny",
        "delhi": "38°C, Hot"
    }

    return weather_data.get(
        city.lower(),
        "Weather information not available."
    )


# -------------------------------------------------------
# LLM
# -------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-5.5",
    api_key="",
    temperature=0
)

# Bind tools
llm_with_tools = llm.bind_tools(
    [calculator, weather]
)

# -------------------------------------------------------
# Take User Input
# -------------------------------------------------------
question = input("Ask your question: ")

messages = [
    HumanMessage(content=question)
]

# -------------------------------------------------------
# Step 1 : LLM decides the tool
# -------------------------------------------------------
ai_message = llm_with_tools.invoke(messages)

# If no tool is required
if not ai_message.tool_calls:
    print("\nAnswer:")
    print(ai_message.content)
    exit()

print("\nTool Selected by LLM:")
print(ai_message.tool_calls[0]["name"])

tool_messages = []

# -------------------------------------------------------
# Step 2 : Execute Tool
# -------------------------------------------------------
available_tools = {
    "calculator": calculator,
    "weather": weather
}

for tool_call in ai_message.tool_calls:

    tool_name = tool_call["name"]

    tool = available_tools[tool_name]

    tool_result = tool.invoke(tool_call["args"])

    tool_messages.append(
        ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        )
    )

# -------------------------------------------------------
# Step 3 : Send Tool Result back to LLM
# -------------------------------------------------------
final_response = llm_with_tools.invoke(
    messages + [ai_message] + tool_messages
)

print("\nFinal Answer:")
print(final_response.content)