from db import init, set_value, get_value
from llm.openai_client import ask

# -----------------------------------------
# Initialize Database
# -----------------------------------------

init()

# -----------------------------------------
# Check Workflow Status
# -----------------------------------------

status = get_value("approval")

# -----------------------------------------
# FIRST RUN
# -----------------------------------------

if status is None:

    query = input("Enter your question: ")

    print("\nPlanner Agent Running...\n")

    plan = ask(
        f"""
You are a Planning Agent.

User Question:
{query}

Create a simple 3-step plan.

Return only the steps.
"""
    )

    print(plan)

    set_value("query", query)
    set_value("plan", plan)
    set_value("approval", "waiting")

    print("\n===================================")
    print("Workflow Paused")
    print("Waiting for Human Approval...")
    print("Call /approve or /reject API")
    print("===================================")

    exit()

# -----------------------------------------
# APPROVED
# -----------------------------------------

elif status == "approved":

    print("\nApproval Received\n")

    query = get_value("query")
    plan = get_value("plan")

    print("Research Agent Running...\n")

    research = ask(
        f"""
You are a Research Agent.

Question:
{query}

Plan:
{plan}

Provide short research notes.
"""
    )

    print(research)

    set_value("research", research)

    print("\nWriter Agent Running...\n")

    final_answer = ask(
        f"""
You are a Writer Agent.

Question:
{query}

Plan:
{plan}

Research:
{research}

Write the final answer.
"""
    )

    print(final_answer)

    set_value("final_answer", final_answer)

    set_value("approval", "completed")

    print("\n===================================")
    print("Workflow Completed Successfully")
    print("===================================")

# -----------------------------------------
# REJECTED
# -----------------------------------------

elif status == "rejected":

    print("\nWorkflow Rejected")
    print("Stopping Execution.")

# -----------------------------------------
# STILL WAITING
# -----------------------------------------

else:

    print(f"\nCurrent Status : {status}")
    print("Workflow is waiting for approval.")