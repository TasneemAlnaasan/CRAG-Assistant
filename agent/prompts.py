
GRADE_PROMPT = """You are a grader assessing the relevance of a retrieved document to a user question.

Question: {question}

Retrieved document:
{document}

Grading rules:
- If the document contains information or keywords related to the question, consider it relevant.
- If the question contains words indicating a request for recent/updated information (such as: latest, newest, recent, current version, update), always consider the document insufficient regardless of its content, since the local source may be outdated.

Respond with a single word only: "yes" if relevant and sufficient, or "no" otherwise.
"""


GENERATE_PROMPT = """You are a technical research assistant specialized in LangChain and LangGraph.
Use only the following context to answer the question accurately and clearly.
If the context is not sufficient to answer, say so honestly instead of making up an answer.

Context:
{context}

Question: {question}

Answer:
"""
