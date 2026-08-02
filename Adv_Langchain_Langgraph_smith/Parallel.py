from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

# ----------------------------
# LLM
# ----------------------------
llm = ChatOpenAI(
    model="gpt-5.5",
    api_key="",
    temperature=0
)

parser = StrOutputParser()

# ----------------------------
# Prompt 1 - Summary
# ----------------------------
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize the following text in 3 lines:\n\n{text}"
)

summary_chain = summary_prompt | llm | parser

# ----------------------------
# Prompt 2 - Keywords
# ----------------------------
keyword_prompt = ChatPromptTemplate.from_template(
    "Extract the top 5 keywords from the following text:\n\n{text}"
)

keyword_chain = keyword_prompt | llm | parser

# ----------------------------
# Parallel Execution
# ----------------------------
parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain
)

# ----------------------------
# User Input
# ----------------------------
text = input("Enter text: ")

result = parallel_chain.invoke({
    "text": text
})

print("\nSummary:")
print(result["summary"])

print("\nKeywords:")
print(result["keywords"])