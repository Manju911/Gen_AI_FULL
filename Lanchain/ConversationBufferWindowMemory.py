from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferWindowMemory

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

# Keep only last 2 messages (k=1 means 1 exchange = 2 messages)
memory = ConversationBufferWindowMemory(k=1, return_messages=True)

print("=== ConversationBufferWindowMemory Demo ===\n")

# Turn 1
print("Turn 1:")
memory.save_context({"input": "Hi, I'm Alice"}, {"output": "Nice to meet you Alice!"})
print(f"Memory: {memory.buffer}\n")

# Turn 2
print("Turn 2:")
memory.save_context({"input": "I like Python"}, {"output": "Python is great!"})
print(f"Memory: {memory.buffer}\n")

# Turn 3 - Old message gets removed!
print("Turn 3:")
memory.save_context({"input": "What's my name?"}, {"output": "I don't know, it was deleted!"})
print(f"Memory: {memory.buffer}\n")

print("=== Explanation ===")
print("k=1 means keep only the last 1 exchange (2 messages)")
print("When we add Turn 3, Turn 1 gets deleted automatically!")