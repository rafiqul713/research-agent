import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from src.state import ResearchState
from src.prompts import (
    PLANNER_PROMPT,
    SUMMARISE_PROMPT,
    WRITER_PROMPT,
    REFLECTION_PROMPT,
)

load_dotenv()

# Initialise LLM and search client once at module level
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",      # free tier
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ── Node 1: Planner ──────────────────────────────────────────────────────────

def planner_node(state: ResearchState) -> dict:
    """Breaks the topic into 3 focused sub-questions."""
    print(f"\n[Planner] Breaking down topic: {state['topic']}")

    prompt = PLANNER_PROMPT.format(topic=state["topic"])
    response = llm.invoke(prompt)

    # Parse numbered list into a Python list
    lines = response.content.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Remove "1. " prefix
            question = line.split(". ", 1)[-1].strip()
            questions.append(question)

    questions = questions[:3]  # cap at 3
    print(f"[Planner] Sub-questions: {questions}")

    return {
        "sub_questions": questions,
        "current_question_index": 0,
        "search_results": [],
        "summaries": [],
        "iteration": 0,
        "report": "",
    }


# ── Node 2: Search ───────────────────────────────────────────────────────────

def search_node(state: ResearchState) -> dict:
    """Searches the web for the current sub-question."""
    idx = state["current_question_index"]
    question = state["sub_questions"][idx]
    print(f"\n[Search] Searching for: '{question}'")

    try:
        response = tavily.search(
            query=question,
            max_results=4,
            search_depth="advanced",   # deeper results on free tier
        )
        snippets = [r["content"] for r in response["results"] if r.get("content")]
        print(f"[Search] Got {len(snippets)} results")
    except Exception as e:
        print(f"[Search] Error: {e}")
        snippets = ["No results found for this query."]

    # Append to existing search results
    existing = state.get("search_results", [])
    return {"search_results": existing + snippets}


# ── Node 3: Summarise ────────────────────────────────────────────────────────

def summarise_node(state: ResearchState) -> dict:
    """Summarises the latest search results for the current sub-question."""
    idx = state["current_question_index"]
    question = state["sub_questions"][idx]

    # Take only the latest batch of results (last 4)
    recent_results = state["search_results"][-4:]
    combined = "\n\n---\n\n".join(recent_results)

    print(f"\n[Summarise] Summarising results for: '{question}'")

    prompt = SUMMARISE_PROMPT.format(question=question, results=combined)
    response = llm.invoke(prompt)
    summary = response.content.strip()

    print(f"[Summarise] Summary length: {len(summary)} chars")

    existing_summaries = state.get("summaries", [])
    return {
        "summaries": existing_summaries + [f"**{question}**\n\n{summary}"],
        "current_question_index": idx + 1,
        "iteration": state.get("iteration", 0) + 1,
    }


# ── Node 4: Reflection (conditional router) ──────────────────────────────────

def reflection_node(state: ResearchState) -> dict:
    """
    Decides whether to keep searching or write the final report.
    This node itself doesn't change state — the conditional edge reads it.
    We use a simple heuristic + optional LLM check.
    """
    idx = state["current_question_index"]
    total = len(state["sub_questions"])
    iteration = state.get("iteration", 0)

    print(f"\n[Reflection] Iteration {iteration}, answered {idx}/{total} questions")

    # Always continue if there are unanswered sub-questions
    if idx < total:
        print("[Reflection] → More questions to answer, continuing search")
        return {"iteration": iteration}

    # All questions answered — optionally ask LLM if we have enough
    if iteration >= total:
        summaries_text = "\n\n".join(state.get("summaries", []))
        prompt = REFLECTION_PROMPT.format(
            topic=state["topic"],
            summaries=summaries_text,
        )
        response = llm.invoke(prompt)
        verdict = response.content.strip().upper()
        print(f"[Reflection] LLM verdict: {verdict}")

    return {"iteration": iteration}


# ── Node 5: Writer ───────────────────────────────────────────────────────────

def writer_node(state: ResearchState) -> dict:
    """Writes the final structured research report."""
    print(f"\n[Writer] Writing final report on: {state['topic']}")

    summaries_text = "\n\n---\n\n".join(state.get("summaries", []))

    prompt = WRITER_PROMPT.format(
        topic=state["topic"],
        summaries=summaries_text,
    )
    response = llm.invoke(prompt)
    report = response.content.strip()

    print(f"[Writer] Report written ({len(report)} chars)")
    return {"report": report}