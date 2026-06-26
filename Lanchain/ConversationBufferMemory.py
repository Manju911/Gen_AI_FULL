from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")
memory = ConversationBufferMemory(return_messages=True)

# Turn 1
user_input = "My name is Alice"
memory.save_context({"input": user_input}, {"output": "Nice to meet you, Alice!"})
print("Turn 1: Saved to memory")

# Turn 2
user_input = "What is my name?"
history = memory.load_memory_variables({})["history"]
print(f"\nTurn 2: History loaded = {len(history)} messages")
for msg in history:
    print(f"  {msg.type}: {msg.content}")

memory.save_context({"input": user_input}, {"output": "Your name is Alice!"})

# Turn 3
print(f"\nTurn 3: Current memory buffer:")
print(memory.buffer)