import faiss
import numpy as np


class FaissRetriever:
    def __init__(self, document_embeddings, documents):
        self.documents = documents

        self.document_embeddings = np.array(
            document_embeddings,
            dtype=np.float32
        )

        if self.document_embeddings.ndim != 2:
            raise ValueError(
                "document_embeddings should be 2-dimensional array."
            )

        if len(self.documents) != len(self.document_embeddings):
            raise ValueError(
                "The number of documents does not match with the number of embeddings."
            )

        if len(self.documents) == 0:
            raise ValueError(
                "There are no documents to create FAISS index."
            )

        normalized_embeddings = self.document_embeddings.copy()

        # Normalize document embeddings using L2 Norm.
        faiss.normalize_L2(normalized_embeddings)

        embedding_dimension = normalized_embeddings.shape[1]  # the number of columns (embedding dimension)

        self.index = faiss.IndexFlatIP(embedding_dimension)  # inner product indicates cosine similarity

        self.index.add(normalized_embeddings)

    def retrieve(self, query_embedding, top_k=3):
        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        if query_embedding.ndim != 2:
            raise ValueError(
                "query_embedding should be a 1-dimensional or 2-dimensional array."
            )

        if query_embedding.shape[1] != self.document_embeddings.shape[1]:
            raise ValueError(
                "The query and document embedding dimensions must match."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        if top_k > len(self.documents):
            top_k = len(self.documents)

        normalized_query = query_embedding.copy()

        # Normalize query embedding using L2 Norm.
        faiss.normalize_L2(normalized_query)

        # Search index with query.
        scores, indices = self.index.search(
            normalized_query,
            top_k
        )

        results = []

        for i in range(top_k):
            document_index = int(indices[0][i])

            if document_index == -1:
                continue

            # Bring document based on document index.
            document = self.documents[document_index]

            result = document.copy()
            result["score"] = float(scores[0][i])

            results.append(result)

        return results
