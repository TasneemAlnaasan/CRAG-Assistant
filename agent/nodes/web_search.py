
from langchain_tavily import TavilySearch
from langchain_core.documents import Document
from agent.state import GraphState
from config.settings import settings

web_search_tool = TavilySearch(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)


def web_search(state: GraphState) -> dict:
    
    question = state["question"]
    documents = state.get("documents", [])

    search_results = web_search_tool.invoke({"query": question})

    web_documents = []
    for result in search_results["results"]:
        doc = Document(
            page_content=result["content"],
            metadata={
                "source": "web",
                "url": result["url"],
            },
        )
        web_documents.append(doc)

    return {"documents": documents + web_documents}
