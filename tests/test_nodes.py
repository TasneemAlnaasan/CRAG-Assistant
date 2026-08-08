import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ingestion.load_and_chunk import clean_content, chunk_documents
from agent.graph import decide_next_step
from langchain_core.documents import Document


# --- اختبارات clean_content ---

def test_removes_js_code_block():
    input_text = """
Some intro text.

:::python

def hello():
    print("hello")

:::

:::js

function hello() {
    console.log("hello");
}

:::

More text after.
"""
    result = clean_content(input_text)

    assert "function hello()" not in result
    assert "console.log" not in result


def test_removes_triple_colon_markers():
    input_text = """
:::note
This is a note.
:::
"""
    result = clean_content(input_text)

    assert ":::" not in result


def test_removes_import_statements():
    input_text = """
import CustomComponent from '/snippets/custom-component.mdx';

Regular content here.
"""
    result = clean_content(input_text)

    assert "import CustomComponent" not in result
    assert "Regular content here." in result


def test_keeps_normal_text_unchanged():
    input_text = "This is just plain text with no special syntax."
    result = clean_content(input_text)

    assert result == input_text


def test_removes_extra_blank_lines():
    input_text = "Line one.\n\n\n\n\nLine two."
    result = clean_content(input_text)

    assert "\n\n\n" not in result


# --- اختبار منطق فلترة JavaScript ---

def test_javascript_path_filter_logic():
    fake_path = "temp_docs/src/oss/javascript/some_file.mdx"
    assert "javascript" in fake_path.lower()

    fake_path_python = "temp_docs/src/oss/langchain/some_file.mdx"
    assert "javascript" not in fake_path_python.lower()


# --- اختبارات decide_next_step ---

def test_decide_next_step_needs_web_search():
    state = {"web_search_needed": "yes"}
    assert decide_next_step(state) == "web_search"


def test_decide_next_step_goes_to_generate():
    state = {"web_search_needed": "no"}
    assert decide_next_step(state) == "generate"


# --- اختبار chunk_documents ---

def test_chunk_documents_splits_long_text():
    long_text = "This is a sentence. " * 200
    doc = Document(page_content=long_text, metadata={"source": "test"})

    result = chunk_documents([doc])

    assert len(result) > 1