import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API Keys (من ملف .env)
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
    LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")

    # LangSmith tracing 
    LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT", "agentic-rag-portfolio")

    # إعدادات ثابتة المشروع 
    VECTOR_DB_PATH = "./chroma_db"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    LLM_MODEL_NAME = "llama-3.3-70b-versatile"

    # إعدادات الـ retrieval
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 4


settings = Settings()