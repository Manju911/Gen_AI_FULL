# from dotenv import load_dotenv
# import os
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# response = client.chat.completions.create(
#     model="gpt-5.5",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is Generative AI?"
#         }
#     ]
# )

# print(response.choices[0].message.content)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.5"
)

response = llm.invoke(
    "What is Generative AI?"
)

print(response.content)