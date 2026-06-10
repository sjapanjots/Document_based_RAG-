from services.vectorstore.faiss_store import FAISSVectorStore


def test_vector_store_returns_highest_similarity(tmp_path) -> None:
    store = FAISSVectorStore(storage_dir=str(tmp_path))
    store.add(
        vectors=[[1.0, 0.0], [0.0, 1.0]],
        texts=["alpha document", "beta document"],
        metadatas=[{"id": "a"}, {"id": "b"}],
    )

    results = store.search([1.0, 0.0], top_k=1)

    assert results[0]["text"] == "alpha document"
    assert results[0]["metadata"]["id"] == "a"
