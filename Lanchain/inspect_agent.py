from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
import requests

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")

@tool
def t(x: str) -> str:
    """Test tool that echoes OK."""
    return "ok"

agent = create_agent(llm, [t], system_prompt="You are a helpful assistant.")

print(type(agent))
print([m for m in dir(agent) if not m.startswith('_')])
