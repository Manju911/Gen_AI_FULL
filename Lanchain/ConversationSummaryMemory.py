from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryMemory

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Memory that summarizes conversation
memory = ConversationSummaryMemory(llm=llm)

print("=== ConversationSummaryMemory Demo ===\n")

# Turn 1
print("Turn 1:")
memory.save_context(
    {"input": "I work at Google as a software engineer"},
    {"output": "That's great! Google is a top tech company."}
)
print(f"Summary: {memory.buffer}\n")

# Turn 2
print("Turn 2:")
memory.save_context(
    {"input": "I have 5 years of experience in Python"},
    {"output": "Wow! You're very experienced with Python."}
)
print(f"Summary: {memory.buffer}\n")

# Turn 3
print("Turn 3:")
memory.save_context(
    {"input": "I'm planning a vacation to Japan"},
    {"output": "Japan is beautiful! Have a great trip."}
)
print(f"Summary: {memory.buffer}\n")

print("=== Explanation ===")
print("Instead of storing all messages, it creates a summary:")
print("'User works at Google as a software engineer with 5 years Python experience'")
print("'User is planning a vacation to Japan'")