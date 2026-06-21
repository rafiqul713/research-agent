# Research Agent

An AI-powered research assistant that takes any topic you give it and returns a structured, well-sourced report — automatically. No copy-pasting from Google, no tab juggling. Just ask, and it researches.


---

## What it actually does

Most "AI research tools" are just a chatbot with a search button. This one is different — it runs a proper agentic loop:

1. **Plans** — it doesn't just search your exact query. It first breaks your topic into 3 focused sub-questions to get better coverage.
2. **Searches** — it queries the web for each sub-question using Tavily, which is purpose-built for LLM agents (cleaner results than raw Google).
3. **Summarises** — raw search results are noisy. After each search, Gemini compresses the findings into a clean, factual summary.
4. **Reflects** — before writing, it checks whether it actually has enough information. If not, it loops back and searches more.
5. **Writes** — once satisfied, it compiles everything into a structured Markdown report with sections, key findings, and a conclusion.

The whole thing runs as a stateful graph using LangGraph, meaning each step passes context to the next — the writer knows everything the searcher found, the reflector knows how many questions have been answered, and so on.

---

## Tech stack

| Layer | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Google Gemini 1.5 Flash (free tier) |
| Web search | Tavily API (free tier) |
| Tracing / observability | LangSmith |
| UI | Streamlit |
| Language | Python 3.11+ |

Everything on the free tier — no credit card needed to try this.

---

## Project structure

```
research-agent/
├── src/
│   ├── state.py        # shared agent state (TypedDict)
│   ├── nodes.py        # each graph node as a Python function
│   ├── graph.py        # LangGraph wiring — nodes + edges
│   └── prompts.py      # all LLM prompts in one place
├── app.py              # Streamlit web UI
├── run.py              # CLI runner (no browser needed)
├── requirements.txt
├── .env  
└── README.md
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/rafiqul713/research-agent.git
cd research-agent
```

### 2. Create a virtual environment

This keeps the project's dependencies completely separate from anything else on your machine. Strongly recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows
```

You'll see `(.venv)` at the start of your terminal prompt. That means it's active.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your free API keys

You need three keys. All are free, none require a credit card.

**Google Gemini**
- Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Sign in with any Google account
- Click "Create API key"
- Copy the key

**Tavily Search**
- Go to [app.tavily.com](https://app.tavily.com)
- Sign up (email or Google)
- Your API key is on the dashboard — copy it

**LangSmith** *(optional but recommended — lets you see what the agent is doing)*
- Go to [smith.langchain.com](https://smith.langchain.com)
- Sign up free
- Go to Settings → API Keys → Create new key

### 5. Set up your environment file

```bash
```

Open `.env` and fill in your keys:

```
GOOGLE_API_KEY=your_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=research-agent
```

### 6. Run it

**Option A — web UI (recommended for first run)**

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501`. Type a topic, hit Research, and watch the agent work through each step in real time.

**Option B — command line**

```bash
python run.py "Impact of AI on software engineering jobs"
```

The report prints to your terminal and saves as a `.md` file in the project folder.

---

## Example output

**Input:** `How is climate change affecting global food security?`

**The agent will:**
- Generate sub-questions like *"Which crops are most threatened by rising temperatures?"*, *"How are droughts affecting grain production in 2024?"*, *"What are governments doing to protect food supply chains?"*
- Search the web for each one
- Summarise the findings
- Write a report with an executive summary, key findings, and conclusion

The whole thing takes about 30–60 seconds.

---

## Observability with LangSmith

If you added a LangSmith key, every run is automatically traced. Go to [smith.langchain.com](https://smith.langchain.com) after running the agent and you'll see:

- Which node ran and in what order
- Exactly what prompt was sent to Gemini
- What Gemini returned
- How long each step took
- Token usage per node

This is what production AI teams use to debug agents. Worth setting up just to see what's happening under the hood.

---

## How to extend this

A few ideas if you want to take it further:

- **Add memory** — store past research sessions in SQLite so the agent can reference previous reports
- **PDF export** — use `fpdf2` or `reportlab` to export the report as a formatted PDF
- **Source citations** — Tavily returns URLs alongside content; thread these through to the final report
- **Multiple search providers** — fall back to SerpAPI if Tavily hits its rate limit
- **Slack or email delivery** — send the finished report somewhere automatically

---

## Common issues

**`ModuleNotFoundError`**
Make sure your virtual environment is active. You should see `(.venv)` in your terminal. If not, run `source .venv/bin/activate`.

**`GOOGLE_API_KEY not found`**
Check that your `.env` file is in the root of the project folder (same level as `app.py`), not inside `src/`.

**Gemini rate limit errors**
The free tier allows about 15 requests per minute. If you hit limits, add `time.sleep(2)` between nodes in `nodes.py`, or wait a minute and try again.

**Tavily returns no results**
Some very niche queries return sparse results. Try broadening your topic slightly.

---

## Requirements

- Python 3.11 or higher
- macOS, Linux, or Windows (WSL recommended on Windows)
- Internet connection (for search and LLM calls)

---

## License

MIT — do whatever you want with this.

---