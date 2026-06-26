from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

summary = ""
history = []

def summarize(conversation_text):
    prompt = f"Summarize this conversation briefly:\n{conversation_text}"
    return llm.invoke([HumanMessage(content=prompt)]).content

def chat(user_input):
    global summary, history

    # Build context from summary + recent history
    messages = []
    if summary:
        messages.append(SystemMessage(content=f"Conversation so far: {summary}"))
    messages += history
    messages.append(HumanMessage(content=user_input))

    response = llm.invoke(messages)
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response.content))

    # Summarize and reset after every 4 messages
    if len(history) >= 4:
        convo_text = "\n".join([f"{m.type}: {m.content}" for m in history])
        summary = summarize(convo_text)
        history = []

    return response.content

print(chat("Hi! My name is Arjun, I am a data scientist from Bangalore."))
print(chat("I have 5 years of experience in Python and ML."))
print(chat("I am learning LangChain now."))
print(chat("Give me a summary of what you know about me."))