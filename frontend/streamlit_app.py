import requests
import streamlit as st


# -----------------------------
# Configuration
# -----------------------------

API_BASE_URL = "http://localhost:8000/api/v1"


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Document RAG Assistant",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------

st.title("📄 Document RAG Assistant")

st.markdown(
    """
    Upload PDF documents and interact with them using AI-powered retrieval.
    """
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("System Status")

    try:
        response = requests.get(
            f"{API_BASE_URL}/health/",
            timeout=5
        )

        if response.status_code == 200:
            st.success("Backend Connected")
        else:
            st.error("Backend Unavailable")

    except Exception:
        st.error("Backend Unavailable")

    st.divider()

    st.write("Version: 1.0.0")


# -----------------------------
# Upload Section
# -----------------------------

st.subheader("Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:
    st.info(
        f"Selected File: {uploaded_file.name}"
    )

    if st.button(
        "Upload Document",
        use_container_width=True
    ):
        st.warning(
            "Upload API not implemented yet."
        )


# -----------------------------
# Chat Section
# -----------------------------

st.divider()

st.subheader("Ask Questions")

question = st.text_input(
    "Enter your question"
)

if st.button(
    "Submit Query",
    use_container_width=True
):
    if not question.strip():
        st.warning(
            "Please enter a question."
        )
    else:
        st.warning(
            "Chat API not implemented yet."
        )


# -----------------------------
# Response Area
# -----------------------------

st.divider()

st.subheader("Response")

st.empty()