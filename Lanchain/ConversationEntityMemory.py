from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationEntityMemory

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Memory that extracts and stores entities
memory = ConversationEntityMemory(llm=llm)

print("=== ConversationEntityMemory Demo ===\n")

# Turn 1 - Extract entities
print("Turn 1:")
user_input_1 = "My name is Alice and I work at Microsoft"
memory.save_context(
    {"input": user_input_1},
    {"output": "Nice to meet you Alice!"}
)

# Load entities with input context
entities_1 = memory.load_memory_variables({"input": user_input_1})
print(f"User: {user_input_1}")
print(f"Entities: {entities_1.get('entities', {})}\n")

# Turn 2 - More entities
print("Turn 2:")
user_input_2 = "I live in New York and love coding"
memory.save_context(
    {"input": user_input_2},
    {"output": "New York is awesome!"}
)

entities_2 = memory.load_memory_variables({"input": user_input_2})
print(f"User: {user_input_2}")
print(f"Entities: {entities_2.get('entities', {})}\n")

# Turn 3
print("Turn 3:")
user_input_3 = "I'm visiting my friend Bob in California"
memory.save_context(
    {"input": user_input_3},
    {"output": "California is beautiful!"}
)

entities_3 = memory.load_memory_variables({"input": user_input_3})
print(f"User: {user_input_3}")
print(f"Entities: {entities_3.get('entities', {})}\n")

# Show all remembered entities
print("=== All Remembered Entities ===")
print(memory.entity_store.store)

print("\n=== Explanation ===")
print("Automatically extracts:")
print("- People: Alice, Bob")
print("- Places: Microsoft, New York, California")
print("- Facts: loves coding")