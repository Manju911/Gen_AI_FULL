from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API Key
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4.1-mini")

# Output Parser
parser = StrOutputParser()

# -------------------------------------------------------
# Step 1: Summarize Customer Review
# -------------------------------------------------------
summary_prompt = ChatPromptTemplate.from_template("""
Summarize the following customer review in one sentence.

Review:
{review}
""")

# -------------------------------------------------------
# Step 2: Perform Sentiment Analysis
# -------------------------------------------------------
sentiment_prompt = ChatPromptTemplate.from_template("""
Analyze the sentiment of the following summary.

Return only one word:
Positive
Negative
Neutral

Summary:
{text}
""")

# -------------------------------------------------------
# Step 3: Recommend an Action
# -------------------------------------------------------
recommend_prompt = ChatPromptTemplate.from_template("""
A customer review has the following sentiment:

{text}

Suggest one action the customer support team should take.
""")

# Create Individual Chains
summary_chain = summary_prompt | llm | parser
sentiment_chain = sentiment_prompt | llm | parser
recommend_chain = recommend_prompt | llm | parser

# Customer Review
review = """
The phone has an excellent camera and beautiful display.
However, the battery drains within a few hours and the device heats up while charging.
"""

# Step 1
summary = summary_chain.invoke({"review": review})
print("=" * 50)
print("SUMMARY")
print("=" * 50)
print(summary)

# Step 2
sentiment = sentiment_chain.invoke({"text": summary})
print("\n" + "=" * 50)
print("SENTIMENT")
print("=" * 50)
print(sentiment)

# Step 3
recommendation = recommend_chain.invoke({"text": sentiment})
print("\n" + "=" * 50)
print("RECOMMENDATION")
print("=" * 50)
print(recommendation)