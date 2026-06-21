from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    # The original research topic from the user
    topic: str

    # Sub-questions the planner breaks the topic into
    sub_questions: List[str]

    # Index tracking which sub-question we're currently searching
    current_question_index: int

    # Raw search result snippets collected so far
    search_results: List[str]

    # Compressed summaries, one per sub-question answered
    summaries: List[str]

    # How many search-summarise loops we've done
    iteration: int

    # The final markdown report
    report: str