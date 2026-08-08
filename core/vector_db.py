
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config.settings import settings


embedding_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)


def build_vector_store(chunks: list[Document]) -> Chroma:
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=settings.VECTOR_DB_PATH,
    )


def load_vector_store() -> Chroma:
    return Chroma(
        persist_directory=settings.VECTOR_DB_PATH,
        embedding_function=embedding_model,
    )


def get_or_create_vector_store(chunks: list[Document] = None) -> Chroma:
    db_exists = os.path.exists(settings.VECTOR_DB_PATH) and os.listdir(settings.VECTOR_DB_PATH)

    if db_exists:
        print("DataBase exists. Loading DataBase..")
        return load_vector_store()

    if chunks is None:
        raise ValueError("Database does not exist, need to build it.")

    print(f"Building a new database from {len(chunks)} chunk...")
    return build_vector_store(chunks)

if __name__ == "__main__":
    from ingestion.load_and_chunk import load_documents, chunk_documents

    docs = load_documents()
    chunks = chunk_documents(docs)

    vs = get_or_create_vector_store(chunks)
    print("Database built/loaded successfully")

    results = vs.similarity_search("what is a LangGraph state", k=2)
    for r in results:
        print(f"\n--- Source: {r.metadata['source']} ---")
        print(r.page_content[:200])