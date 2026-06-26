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

resp = agent.invoke({"input":"Hello"})
print('TYPE:', type(resp))
try:
    print('REPR:', repr(resp))
except Exception as e:
    print('REPR ERROR', e)

# If it's dict-like, print keys
try:
    print('GETATTR dir:', dir(resp))
    if hasattr(resp, 'keys'):
        print('keys:', list(resp.keys()))
except Exception as e:
    print('ERROR printing keys', e)
