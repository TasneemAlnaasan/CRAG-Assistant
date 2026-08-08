import streamlit as st
from agent.graph import app_graph

st.set_page_config(page_title="CRAG Assistant", page_icon="🔍")

st.title("🔍 CRAG Assistant")
st.caption("Ask questions about LangChain and LangGraph — powered by Agentic RAG (Corrective RAG pattern)")

with st.form("question_form"):
    question = st.text_input("Your question:", placeholder="e.g. What is a LangGraph node?")
    submitted = st.form_submit_button("Ask")

if submitted and question:
    with st.spinner("Thinking..."):
        result = app_graph.invoke({"question": question})

    st.markdown("### Answer")
    st.markdown(result["generation"])

    with st.expander("📚 Sources"):
        for i, doc in enumerate(result["documents"], start=1):
            source = doc.metadata.get("source", "unknown")
            if source == "web":
                url = doc.metadata.get("url", "")
                st.markdown(f"**{i}.** 🌐 Web — [{url}]({url})")
            else:
                file_path = doc.metadata.get("file_path", "")
                st.markdown(f"**{i}.** 📄 {source} — `{file_path}`")