PLANNER_PROMPT = """You are a research planner. A user wants to research the following topic:

Topic: {topic}

Break this into exactly 3 focused, specific sub-questions that together will give 
a thorough understanding of the topic. Each sub-question should target a different 
angle (e.g. current state, challenges, future outlook).

Return ONLY a numbered list like:
1. First sub-question
2. Second sub-question
3. Third sub-question

No preamble, no explanation."""


SUMMARISE_PROMPT = """You are a research analyst. Below are web search results for the question:

Question: {question}

Search results:
{results}

Write a concise 150-200 word summary of the key findings relevant to the question.
Include specific facts, numbers, and names where available.
Do not add opinions. End with one sentence on what is still uncertain."""


WRITER_PROMPT = """You are an expert research writer. Write a well-structured research report on:

Topic: {topic}

Use ONLY the following research summaries as your source material:

{summaries}

Format the report in Markdown with these exact sections:
# {topic}

## Executive Summary
(3-4 sentences covering the most important findings)

## Key Findings

### [Finding 1 title]
...

### [Finding 2 title]
...

### [Finding 3 title]
...

## Conclusion
(2-3 sentences on the overall picture and what to watch)

## Sources used
(List the sub-questions that were researched)

Be specific. Use facts from the summaries. Do not fabricate information."""


REFLECTION_PROMPT = """You are a critical research reviewer.

Topic being researched: {topic}
Summaries gathered so far:
{summaries}

Is the research sufficient to write a comprehensive report on this topic?
Answer with ONLY one word: YES or NO.
- YES if we have covered the main angles with specific facts
- NO if major aspects are still missing or vague"""