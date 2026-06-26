from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

history = []
WINDOW_SIZE = 4  # keep last 4 messages (2 exchanges)

def chat(user_input):
    history.append(HumanMessage(content=user_input))
    # Only send last WINDOW_SIZE messages
    windowed = history[-WINDOW_SIZE:]
    response = llm.invoke(windowed)
    history.append(AIMessage(content=response.content))
    return response.content

print(chat("My name is Arjun."))
print(chat("I live in Bangalore."))
print(chat("I love cricket."))
print(chat("What is my name?"))  # Might forget if window too small