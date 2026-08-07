
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings


def load_documents(base_path: str = "temp_docs/src/oss") -> list[Document]:
    """
    يمشي جوه مجلدي langchain و langgraph،
    يقرا كل ملف .mdx، ويحوّله لـ Document object.
    """
    target_folders = ["langchain", "langgraph"]
    documents = []

    for folder_name in target_folders:
        folder_path = Path(base_path) / folder_name

        for file_path in folder_path.rglob("*.mdx"):
            content = file_path.read_text(encoding="utf-8")

            if not content.strip():
                continue

            doc = Document(
                page_content=content,
                metadata={
                    "source": folder_name,
                    "file_path": str(file_path),
                },
            )
            documents.append(doc)

    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    يقسّم كل document لقطع أصغر حسب الإعدادات في settings.py
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


if __name__ == "__main__":
    docs = load_documents()
    print(f"Number of loaded files: {len(docs)}")

    chunks = chunk_documents(docs)
    print(f"Number of chunks after splitting: {len(chunks)}")

    langchain_count = sum(1 for c in chunks if c.metadata["source"] == "langchain")
    langgraph_count = sum(1 for c in chunks if c.metadata["source"] == "langgraph")
    print(f" LangChain: {langchain_count} |  LangGraph: {langgraph_count}")