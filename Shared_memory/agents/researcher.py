from llm.openai_client import ask
def run(mem,sid):
    p=mem.read(sid,'plan')
    notes=ask(f"Research:\n{p['query']}\nPlan:{p['plan']}")
    mem.write(sid,'research',{'notes':notes})
