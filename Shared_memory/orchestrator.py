import uuid
from memory.shared_memory import SharedMemory
from agents import planner,researcher,writer
def execute(query):
    mem=SharedMemory();sid=str(uuid.uuid4())
    planner.run(mem,sid,query)
    researcher.run(mem,sid)
    writer.run(mem,sid)
    return mem.read(sid,'final')['answer']
