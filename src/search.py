import numpy as np


def search_top_k(
        query_embedding: np.ndarray,
        document_embeddings: np.ndarray,
        documents: list[str],
        top_k: int = 3,
) -> list[tuple[str, float]]:
    """Return Top-K similar document with query."""
    if len(documents) == 0:
        return []

    if len(documents) != len(document_embeddings):
        raise ValueError("The number of documents does not match with the number of embeddings.")

    similarities = document_embeddings @ query_embedding

    top_k = min(top_k, len(documents))
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = [
        (documents[index], float(similarities[index]))
        for index in top_indices
    ]

    return results
