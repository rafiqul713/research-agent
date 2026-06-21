"""Streamlit UI for the Research Agent."""

import streamlit as st
from dotenv import load_dotenv
from src.graph import research_app

load_dotenv()

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide",
)

st.title("Research Agent")
st.caption("Powered by LangGraph + Gemini + Tavily")

# Sidebar shows the agent internals
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. **Planner** — breaks your topic into 3 sub-questions
    2. **Search** — queries Tavily for each question
    3. **Summarise** — compresses results with Gemini
    4. **Reflection** — decides if we need more research
    5. **Writer** — compiles the final report
    """)
    st.divider()
    st.caption("Built with LangGraph · Gemini 1.5 Flash · Tavily")

topic = st.text_input(
    "Enter a research topic",
    placeholder="e.g. How is AI changing software engineering jobs in 2025?",
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button("Research", type="primary", use_container_width=True)

if run and topic:
    with st.status("Agent is working...", expanded=True) as status:
        st.write("Planning sub-questions...")

        # Stream node-by-node updates
        final_state = None
        for step in research_app.stream({"topic": topic}):
            node_name = list(step.keys())[0]
            node_output = step[node_name]

            if node_name == "planner":
                questions = node_output.get("sub_questions", [])
                st.write(f"Sub-questions: {questions}")

            elif node_name == "search":
                st.write("Searching the web...")

            elif node_name == "summarise":
                summaries = node_output.get("summaries", [])
                st.write(f"Summarised {len(summaries)} question(s)")

            elif node_name == "reflection":
                st.write("Checking if we have enough research...")

            elif node_name == "write_report":
                st.write("Writing final report...")
                final_state = node_output

        status.update(label="Done!", state="complete")

    if final_state and final_state.get("report"):
        st.divider()
        st.markdown(final_state["report"])

        st.download_button(
            label="Download report",
            data=final_state["report"],
            file_name=topic[:40].replace(" ", "_") + "_report.md",
            mime="text/markdown",
        )
    else:
        # Fallback: invoke instead of stream
        result = research_app.invoke({"topic": topic})
        st.markdown(result.get("report", "No report generated."))