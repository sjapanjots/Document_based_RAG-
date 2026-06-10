import requests
import streamlit as st


API_BASE_URL = "http://localhost:8000/api/v1"

if "document_indexed" not in st.session_state:
    st.session_state["document_indexed"] = False


st.set_page_config(
    page_title="Document RAG Assistant",
    page_icon="DOC",
    layout="wide",
)

st.title("Document RAG Assistant")
st.markdown("Upload PDF documents and ask grounded questions over their content.")

with st.sidebar:
    st.header("System Status")
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        if response.status_code == 200:
            st.success("Backend Connected")
        else:
            st.error("Backend Unavailable")
    except Exception:
        st.error("Backend Unavailable")

    st.divider()
    st.write("Version: 1.0.0")

st.subheader("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    st.info(f"Selected File: {uploaded_file.name}")

    if st.button("Upload Document", use_container_width=True):
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }
        try:
            response = requests.post(
                f"{API_BASE_URL}/upload/",
                files=files,
                timeout=60,
            )
            if response.ok:
                payload = response.json()
                st.session_state["document_indexed"] = True
                st.success(
                    f"Indexed {payload['filename']} "
                    f"({payload['chunk_count']} chunks)"
                )
            else:
                st.error(response.json().get("detail", "Upload failed."))
        except Exception as exception:
            st.error(f"Upload failed: {exception}")

st.divider()
st.subheader("Ask Questions")

question = st.text_input("Enter your question")

if st.button("Submit Query", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not st.session_state["document_indexed"]:
        st.warning("Upload and index a PDF before asking questions.")
    else:
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/",
                json={"question": question},
                timeout=60,
            )
            if response.ok:
                payload = response.json()
                st.session_state["last_answer"] = payload["answer"]
                st.session_state["last_sources"] = payload["sources"]
                if not payload["sources"]:
                    st.warning("No indexed document chunks were found. Upload the PDF again.")
            else:
                st.error(response.json().get("detail", "Chat failed."))
        except Exception as exception:
            st.error(f"Chat failed: {exception}")

st.divider()
st.subheader("Response")

if "last_answer" in st.session_state:
    st.write(st.session_state["last_answer"])

    sources = st.session_state.get("last_sources", [])
    if sources:
        with st.expander("Sources"):
            for source in sources:
                metadata = source["metadata"]
                st.caption(
                    f"{metadata.get('filename', 'document')} "
                    f"chunk {metadata.get('chunk_index', 0)} "
                    f"score {source['score']:.3f}"
                )
                st.write(source["text"])
else:
    st.empty()
