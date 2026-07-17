import hashlib
from pathlib import Path

import numpy as np


class EmbeddingCache:
    def __init__(self, cache_path):
        self.cache_path = Path(cache_path)

    def create_cache_key(self, documents, model_name):
        hasher = hashlib.sha256()

        hasher.update(model_name.encode("utf-8"))

        for document in documents:
            source = document["source"]
            chunk_id = str(document["chunk_id"])
            text = document["text"]

            hasher.update(source.encode("utf-8"))
            hasher.update(chunk_id.encode("utf-8"))
            hasher.update(text.encode("utf-8"))

        return hasher.hexdigest()

    def load(self, cache_key):
        if not self.cache_path.exists():
            return None

        try:
            cache_data = np.load(self.cache_path)

            saved_key = str(cache_data["cache_key"])
            embeddings = cache_data["embeddings"]

            if saved_key != cache_key:
                return None

            return embeddings

        except (OSError, ValueError, KeyError):
            return None

    def save(self, cache_key, embeddings):
        self.cache_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        np.savez(
            self.cache_path,
            cache_key=cache_key,
            embeddings=embeddings
        )
