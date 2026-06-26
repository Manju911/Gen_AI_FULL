import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent 

load_dotenv()

# 1. Initialize LLM (Using a standard tool-calling model)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Define the Tool
@tool
def get_country_info(country: str) -> str:
    """
    Get information about a country. Use this tool when asked about specific countries.
    """
    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        response = requests.get(url)
        data = response.json()[0]

        capital = data.get("capital", ["N/A"])[0]
        population = data.get("population", "N/A")
        region = data.get("region", "N/A")

        return (
            f"Country: {country}\n"
            f"Capital: {capital}\n"
            f"Population: {population}\n"
            f"Region: {region}"
        )
    except Exception as e:
        return f"Error fetching data for {country}: {str(e)}"

tools = [get_country_info]

# 3. Create the Agent (Using 'prompt' instead of 'state_modifier')
system_prompt = "You are a helpful assistant. Always use your tools to look up country data."
agent = create_react_agent(llm, tools, prompt=system_prompt)

# 4. Invoke the Agent
response = agent.invoke(
    {
        "messages": [("user", "Tell me about India")]
    }
)

print("\nFinal Answer:")
msgs = response.get("messages", [])
if msgs:
    # Print the last assistant message content
    print(msgs[-1].content)
else:
    print(response)