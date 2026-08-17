import requests
import streamlit as st


# API_URL = "http://localhost:8000"
API_URL = "http://api:8000"


st.set_page_config(
    page_title="AI IT Support",
    page_icon="🛠️"
)


st.title("🛠️ AI IT Support Assistant")

st.write(
    "Ask an IT support question."
)


question = st.text_area(
    "Describe your problem"
)


if st.button("Ask AI"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "AI agents are working..."
        ):

            response = requests.post(
                f"{API_URL}/support",
                json={
                    "question": question
                },
                timeout=60
            )

        if response.status_code == 200:

            data = response.json()

            st.success(
                f"Agent: {data.get('agent')}"
            )

            st.write(
                data.get("answer")
                or data.get("message")
            )

            st.caption(
                f"Category: {data.get('category')}"
            )

            if data.get("task_id"):

                st.info(
                    "Background ticket task started."
                )

        else:

            st.error(
                response.text
            )