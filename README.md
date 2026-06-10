# Enterprise Document Intelligence Assistant

A FastAPI and Streamlit Retrieval Augmented Generation application for uploading
PDFs, indexing chunks, retrieving relevant passages, and answering questions
with Gemini.

## Features

- PDF upload and text extraction with PyMuPDF
- Recursive and sliding-window chunking strategies
- Sentence Transformers embeddings with deterministic local fallback
- FAISS vector search with NumPy fallback
- Gemini response generation with context-only prompting
- FastAPI backend and Streamlit frontend
- Docker-ready backend

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Backend API: `http://localhost:8000/api/v1`

## Environment

Create a `.env` file to enable Gemini:

```env
GEMINI_API_KEY=your_api_key_here
```

The app still works without a key by returning the most relevant retrieved
document context.

## Test

```bash
pytest -q
```
