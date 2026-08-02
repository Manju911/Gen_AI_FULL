from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
    RunnableBranch
)

# Step 1: Convert to uppercase
uppercase = RunnableLambda(
    lambda x: {
        "text": x.upper()
    }
)

# Step 2: Preserve data and add original text
passthrough = RunnablePassthrough.assign(
    original=lambda x: x["text"]
)

# Step 3: Run multiple tasks simultaneously
parallel = RunnableParallel(
    uppercase=RunnableLambda(
        lambda x: x["text"]
    ),
    length=RunnableLambda(
        lambda x: len(x["text"])
    ),
    reverse=RunnableLambda(
        lambda x: x["text"][::-1]
    )
)

# Step 4: Conditional routing
branch = RunnableBranch(
    (
        lambda x: x["length"] > 8,
        RunnableLambda(
            lambda x: {
                **x,
                "category": "Long Text"
            }
        )
    ),
    RunnableLambda(
        lambda x: {
            **x,
            "category": "Short Text"
        }
    )
)

# LCEL Pipeline
chain = (
    uppercase
    | passthrough
    | parallel
    | branch
)

result = chain.invoke("LangChain")

print(result)