from langgraph.graph import StateGraph, END
from agent.state import GraphState
from agent.routing import decide_next_step
from agent.nodes.retrieve import retrieve
from agent.nodes.grade import grade
from agent.nodes.web_search import web_search
from agent.nodes.generate import generate


workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")

workflow.add_edge("retrieve", "grade")

workflow.add_conditional_edges(
    "grade",
    decide_next_step,
    {
        "web_search": "web_search",
        "generate": "generate",
    },
)

workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()


if __name__ == "__main__":
    result = app_graph.invoke({"question": "What is a LangGraph node?"})
    print("\n=== Answer ===")
    print(result["generation"])
    print("\n=== Sources ===")
    for doc in result["documents"]:
        print(f"- {doc.metadata.get('source')}")