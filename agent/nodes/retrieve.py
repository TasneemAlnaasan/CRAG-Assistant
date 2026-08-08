
from agent.state import GraphState
from core.vector_db import load_vector_store
from config.settings import settings

vector_store = load_vector_store()


def retrieve(state: GraphState) -> dict:
    
    question = state["question"]

    documents = vector_store.similarity_search(
        question,
        k=settings.TOP_K_RESULTS,
    )

    return {"documents": documents}