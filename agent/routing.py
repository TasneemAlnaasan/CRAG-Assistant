
from agent.state import GraphState


def decide_next_step(state: GraphState) -> str:
    
    if state["web_search_needed"] == "yes":
        return "web_search"
    return "generate"