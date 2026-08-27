import os

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖"
)


st.title("🤖 AI Assistant")

st.write(
    "Ask any question and get an AI-powered response."
)


api_key = os.getenv("OPENAI_API_KEY")


if not api_key:

    st.error(
        "OPENAI_API_KEY is not configured."
    )

    st.stop()


client = OpenAI(
    api_key=api_key
)


question = st.text_area(
    "Ask your question",
    placeholder="Example: What is Cloud Run?"
)


if st.button("Ask AI"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "AI is thinking..."
        ):

            try:

                response = client.chat.completions.create(
                    model="gpt-5.5",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful AI assistant. "
                                "Answer clearly and simply."
                            )
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                st.subheader("Answer")

                st.write(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )