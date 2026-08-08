
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent.state import GraphState
from agent.prompts import GRADE_PROMPT
from config.settings import settings

llm = ChatGroq(model=settings.LLM_MODEL_NAME, api_key=settings.GROQ_API_KEY)
grade_prompt_template = ChatPromptTemplate.from_template(GRADE_PROMPT)
grader_chain = grade_prompt_template | llm


def grade(state: GraphState) -> dict:
    
    question = state["question"]
    documents = state["documents"]

    relevant_documents = []

    for doc in documents:
        result = grader_chain.invoke({
            "question": question,
            "document": doc.page_content,
        })
        grade_result = result.content.strip().lower()

        if grade_result == "yes":
            relevant_documents.append(doc)

    if len(relevant_documents) > 0:
        web_search_needed = "no"
    else:
        web_search_needed = "yes"

    return {
        "documents": relevant_documents,
        "web_search_needed": web_search_needed,
    }