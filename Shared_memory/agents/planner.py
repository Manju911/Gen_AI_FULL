from llm.openai_client import ask
def run(mem,sid,query):
    plan=ask(f'Break into steps:\n{query}')
    mem.write(sid,'plan',{'query':query,'plan':plan})
