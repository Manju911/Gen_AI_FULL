# from llm.openai_client import ask
# def run(mem,sid):
#     p=mem.read(sid,'plan');r=mem.read(sid,'research')
#     ans=ask(f"Write final answer. Query:{p['query']}\nPlan:{p['plan']}\nResearch:{r['notes']}")
#     mem.write(sid,'final',{'answer':ans})


from pathlib import Path

from llm.openai_client import ask


def run(mem, sid):
    # Read data from shared memory
    plan = mem.read(sid, "plan")
    research = mem.read(sid, "research")

    # Generate final answer using the LLM
    ans = ask(
        f"""
Write a detailed final answer.

User Query:
{plan['query']}

Plan:
{plan['plan']}

Research:
{research['notes']}
"""
    )

    # Save final answer into shared memory
    mem.write(
        sid,
        "final",
        {
            "answer": ans
        }
    )

    # Create output directory if it doesn't exist
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Save final answer as a text file
    file_path = output_dir / f"{sid}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("========== FINAL ANSWER ==========\n\n")
        file.write(f"Session ID : {sid}\n\n")
        file.write(f"User Query : {plan['query']}\n\n")
        file.write(ans)

    print(f"\nFinal answer saved to: {file_path}")
