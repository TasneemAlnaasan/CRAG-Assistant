
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agent.state import GraphState
from agent.prompts import GENERATE_PROMPT
from config.settings import settings

llm = ChatGroq(model=settings.LLM_MODEL_NAME, api_key=settings.GROQ_API_KEY)
generate_prompt_template = ChatPromptTemplate.from_template(GENERATE_PROMPT)
generate_chain = generate_prompt_template | llm


def generate(state: GraphState) -> dict:
    
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join(doc.page_content for doc in documents)

    result = generate_chain.invoke({
        "context": context,
        "question": question,
    })

    return {"generation": result.content}