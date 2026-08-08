
from typing import TypedDict, List
from langchain_core.documents import Document


class GraphState(TypedDict):
    
    question: str              # user's question
    documents: List[Document]  # chunks from retriever
    generation: str            # final answer
    web_search_needed: str     # grader decision "yes" or "no"  