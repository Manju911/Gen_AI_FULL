# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# load_dotenv()

# llm = ChatOpenAI(model="gpt-5.5")

# prompt = PromptTemplate(
#     template="Explain {topic} in simple terms",
#     input_variables=["topic"]
# )

# chain = prompt | llm | StrOutputParser()

# response = chain.invoke({
#     "topic": "Machine Learning"
# })

# print(response)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")

# Step 1
explain_prompt = PromptTemplate(
    template="Explain {topic} in detail",
    input_variables=["ml"]
)

# Step 2
summary_prompt = PromptTemplate(
    template="""
    Summarize the following text in 3 bullet points:

    {text}
    """,
    input_variables=["ml"]
)

explain_chain = explain_prompt | llm | StrOutputParser()
summary_chain = summary_prompt | llm | StrOutputParser()

# Execute Step 1
explanation = explain_chain.invoke({
    "topic": "Vector Databases"
})

# Execute Step 2
summary = summary_chain.invoke({
    "text": explanation
})

print(summary)