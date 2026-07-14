import numpy as np


def search_top_k(
        query_embedding,
        document_embeddings,
        documents,
        top_k=3,
):
    # Return Top-K similar document with query.
    if len(documents) == 0:
        return []

    if len(documents) != len(document_embeddings):
        raise ValueError("The number of documents does not match with the number of embeddings.")

    similarities = document_embeddings @ query_embedding

    top_k = min(top_k, len(documents))

    sorted_indices = np.argsort(similarities)
    descending_indices = sorted_indices[::-1]
    top_indices = descending_indices[:top_k]

    results = []

    for index in top_indices:
        document = documents[index]
        score = float(similarities[index])

        result = {
            "text": document["text"],
            "source": document["source"],
            "chunk_id": document["chunk_id"],
            "score": score,
        }

        results.append(result)

    return results
