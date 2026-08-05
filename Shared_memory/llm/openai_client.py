from openai import OpenAI
from config import OPENAI_API_KEY,MODEL
client=OpenAI(api_key=OPENAI_API_KEY)
def ask(prompt):
    r=client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content
