import os
import uuid
import requests
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai import LLM
from langchain_openai import ChatOpenAI

# =====================================================
# Load API Key
# =====================================================

load_dotenv()

llm = LLM(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

# =====================================================
# Tools
# =====================================================

@tool("Calculator")
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions."""

    print("\n>>> Calculator Tool Called")

    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return str(e)


@tool("Weather")
def weather(city: str) -> str:
    """Get current weather."""

    print("\n>>> Weather Tool Called")

    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    if "results" not in geo:
        return "City not found."

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    data = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
    ).json()

    current = data["current"]

    return (
        f"Temperature : {current['temperature_2m']}°C\n"
        f"Wind Speed : {current['wind_speed_10m']} km/h"
    )


@tool("Random Joke")
def joke(_: str = "") -> str:
    """Return a random joke."""

    print("\n>>> Joke Tool Called")

    data = requests.get(
        "https://official-joke-api.appspot.com/random_joke"
    ).json()

    return f"{data['setup']}\n\n{data['punchline']}"


@tool("UUID Generator")
def generate_uuid(_: str = "") -> str:
    """Generate UUID."""

    print("\n>>> UUID Tool Called")

    return str(uuid.uuid4())


# =====================================================
# Agent
# =====================================================

assistant = Agent(
    role="AI Assistant",
    goal="Help users",
    backstory="Helpful assistant",
    llm=llm,
    tools=[calculator, weather, joke, generate_uuid],
    verbose=True,
)

# =====================================================
# Chat Loop
# =====================================================

print("=" * 60)
print("CrewAI Agent Started")
print("=" * 60)

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    task = Task(
        description=question,
        expected_output="Answer the user's question.",
        agent=assistant,
    )

    crew = Crew(
        agents=[assistant],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\nAssistant :", result)