from langgraph.graph import StateGraph, END
from src.state import ResearchState
from src.nodes import (
    planner_node,
    search_node,
    summarise_node,
    reflection_node,
    writer_node,
)


def should_continue(state: ResearchState) -> str:
    """
    Conditional edge function.
    Returns the name of the next node to run.
    """
    idx = state["current_question_index"]
    total = len(state["sub_questions"])

    if idx < total:
        return "search"       # still have sub-questions to answer
    else:
        return "write_report" # all done, write the report


def build_graph():
    graph = StateGraph(ResearchState)

    # Register every node
    graph.add_node("planner",      planner_node)
    graph.add_node("search",       search_node)
    graph.add_node("summarise",    summarise_node)
    graph.add_node("reflection",   reflection_node)
    graph.add_node("write_report", writer_node)

    # Entry point
    graph.set_entry_point("planner")

    # Fixed edges
    graph.add_edge("planner",   "search")
    graph.add_edge("search",    "summarise")
    graph.add_edge("summarise", "reflection")

    # Conditional edge: reflection decides what comes next
    graph.add_conditional_edges(
        "reflection",
        should_continue,
        {
            "search":       "search",       # loop back
            "write_report": "write_report", # exit loop
        },
    )

    # Writer is the final node
    graph.add_edge("write_report", END)

    return graph.compile()


# Build once, import everywhere
research_app = build_graph()