from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(
            self,
            model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def encode_documents(self, documents):
        # Embed various documents and return as normalized NumPy array.
        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings

    def encode_query(self, query):
        # Embed one query and return as normalized vector.
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding
