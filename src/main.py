from pathlib import Path

from embedder import TextEmbedder
from embedding_cache import EmbeddingCache
from document_loader import load_document
from prompt_builder import build_prompt
from retriever import FaissRetriever
from generator import AnswerGenerator


def main():
    project_root = Path(__file__).resolve().parent.parent
    cache_path = project_root / "cache" / "embeddings.npz"

    source = input("Enter document path: ").strip()

    if not source:
        print("Please enter a document path.")
        return

    source_path = Path(source)

    if not source_path.is_absolute():
        source_path = project_root / source_path

    try:
        documents = load_document(source_path)

    except (FileNotFoundError, ValueError) as error:
        print(error)
        return

    print(f"{len(documents)} chunks loaded.\n")

    document_texts = []

    for document in documents:
        document_texts.append(document["text"])

    print("Loading embedding model...")
    embedder = TextEmbedder()
    print("Embedding model loaded.\n")

    embedding_cache = EmbeddingCache(cache_path)

    cache_key = embedding_cache.create_cache_key(
        documents,
        embedder.model_name,
    )

    document_embeddings = embedding_cache.load(cache_key)

    # Cache does not exist.
    if document_embeddings is None:
        print("Generating document embeddings...")

        document_embeddings = embedder.encode_documents(document_texts)

        embedding_cache.save(
            cache_key,
            document_embeddings,
        )

        print("Document embeddings generated and saved to cache.\n")
    else:
        print("Document embeddings loaded from cache.\n")

    print("Creating FAISS index...")
    retriever = FaissRetriever(
        document_embeddings,
        documents,
    )
    print("FAISS index created.\n")

    generator = AnswerGenerator()

    threshold = 0.1
    top_k = 3

    while True:
        query = input("\nEnter query(q to quit): ").strip()

        if query.lower() == "q":  # Q or q
            print("Program terminated.")
            break

        if not query:
            print("Please enter a query.")
            continue

        # Encode query.
        query_embedding = embedder.encode_query(query)

        # Search index based on query and retrieve top k results.
        results = retriever.retrieve(
            query_embedding,
            top_k,
        )

        filtered_results = []

        for result in results:
            if result["score"] >= threshold:
                filtered_results.append(result)

        if len(filtered_results) == 0:
            print("\nNo relevant documents found.")
            continue

        print("\nSearch results")

        rank = 1

        for result in filtered_results:
            print(f"\nRank: {rank} | Similarity: {result['score']:.4f}")

            print(f"Source: {result['source']} " f"| Chunk: {result['chunk_id']}")

            print(result["text"])

            rank += 1

        # Build prompt based on query and filtered results.
        prompt = build_prompt(query, filtered_results, )

        print("\nGenerating answer...")

        # Generate answer based on prompt.
        answer = generator.generate(prompt)

        print("\nGenerated answer")
        print(answer)


if __name__ == "__main__":
    main()
