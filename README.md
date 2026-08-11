
# 🔍 CRAG Assistant

An agentic RAG system that answers questions about LangChain and LangGraph documentation — built with the Corrective RAG (CRAG) pattern.

**Live demo:** [https://hehnvtn5jnvqnxaelaepmm.streamlit.app/]

## What makes this different from regular RAG

Most RAG systems retrieve documents and generate an answer, no matter how relevant the retrieved content actually is. CRAG Assistant adds a self-checking step: after retrieving documents from the local knowledge base, an LLM grades their relevance to the question. If the local documents aren't sufficient — either because they're irrelevant or because the question asks for recent/updated information — the agent automatically falls back to a live web search instead of generating an unreliable answer.

## Architecture

```
User Question
     │
     ▼
 [Retrieve] ──► searches ChromaDB (LangChain + LangGraph docs)
     │
     ▼
  [Grade] ──► LLM evaluates relevance of each retrieved document
     │
     ├── relevant? ──► [Generate] ──► Answer
     │
     └── not relevant / outdated? ──► [Web Search] ──► [Generate] ──► Answer
```

Built as a graph with [LangGraph](https://github.com/langchain-ai/langgraph), where each step is a node and the grading step determines the path via a conditional edge.

## Tech Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq (Llama 3.3 70B) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector store | ChromaDB |
| Web search fallback | Tavily |
| UI | Streamlit |
| Observability | LangSmith |
| CI | GitHub Actions |

Every tool used is free-tier.

## Knowledge Base

The local knowledge base is built from the official [LangChain/LangGraph documentation](https://github.com/langchain-ai/docs) (Python only — JavaScript content is filtered out during ingestion), cleaned of documentation-specific syntax (Mintlify component tags, import statements, multi-language code tabs) before chunking.

## Running Locally

```bash
# 1. Clone this repo
git clone https://github.com/TasneemAlnaasan/CRAG-Assistant.git
cd YOUR_REPO_NAME

# 2. Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Add your API keys to .env (see .env.example)
cp .env.example .env
# then fill in GROQ_API_KEY, TAVILY_API_KEY, LANGCHAIN_API_KEY

# 4. Build the knowledge base
git clone --depth 1 https://github.com/langchain-ai/docs.git temp_docs
python -m core.vector_db

# 5. Run the app
streamlit run app.py
```

## Running Tests

```bash
pytest tests/ -v
```

Tests cover the pure logic (content cleaning, routing decisions, chunking) without calling external APIs, so they run safely in CI on every push.

## Example

**Question:** What is a LangGraph node?

**Answer:** A LangGraph node is nothing more than a function. It can contain a Large Language Model (LLM) or just standard code, and its primary role is to perform work. Nodes are the components that execute operations in a LangGraph workflow.

**Sources:** langgraph, langgraph, langgraph *(all from local knowledge base — no web search needed)*

## Future Improvements

- Mock external API calls (Groq, Tavily) to unit test the `grade`, `generate`, and `web_search` nodes without hitting live APIs
- Schedule periodic `git pull` + re-ingestion to keep the local knowledge base current
- Dockerize the build so the vector database is baked into the image at build time (useful for platforms with ephemeral storage, like Render)
- Extend the grading step to detect outdated information more precisely, beyond keyword-based triggers