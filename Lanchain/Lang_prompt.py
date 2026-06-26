# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

# load_dotenv()

# llm = ChatOpenAI(
#     model="gpt-5.5"
# )

# prompt = PromptTemplate(
#     template="Explain {topic} in simple terms",
#     input_variables=["topic"]
# )

# formatted_prompt = prompt.format(
#     topic="ML"
# )

# response = llm.invoke(formatted_prompt)

# print(response.content)

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")

prompt = PromptTemplate(
    template="""
    Explain {topic}
    for {audience}.
    """,
    input_variables=["topic", "audience"]
)

# Create Chain
chain = prompt | llm

response = chain.invoke({
    "topic": "Machine Learning",
    "audience": "fruit seller"
})

print(response.content)