import streamlit as st
from agent import agent_executor

st.set_page_config(
    page_title="Study Schedule AI 📚",
    layout="wide"
)

st.title("📚 Study Schedule AI Agent")

query = st.text_input(
    "Ask anything about your schedule, lectures, or exams"
)

if st.button("Ask") and query:

    with st.spinner("Thinking... 🤖"):

        try:

            result = agent_executor.invoke({
                "input": query
            })

            st.success("Answer")

            st.write(result["output"])

        except Exception:

            st.error("API quota exceeded. Try again later.")