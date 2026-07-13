from pathlib import Path

from embed import TextEmbedder
from load_data import load_paragraphs
from search import search_top_k


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "sample.txt"

    documents = load_paragraphs(str(data_path))

    print(f"{len(documents)} paragraphs loaded.")

    print("Loading embedding model...")
    embedder = TextEmbedder()
    print("Embedding model loaded.")

    print("Generating document embeddings...")
    document_embeddings = embedder.encode_documents(documents)
    print("Document embeddings generated.")

    while True:
        query = input("\nEnter query(q to quit): ").strip()

        if query.lower() == "q":
            print("Program terminated.")
            break

        if not query:
            print("Please enter a query.")
            continue

        query_embedding = embedder.encode_query(query)
        results = search_top_k(
            query_embedding=query_embedding,
            document_embeddings=document_embeddings,
            documents=documents,
            top_k=3,
        )

        THRESHOLD = 0.3

        filtered_results = [
            (doc, score)
            for doc, score in results
            if score >= THRESHOLD
        ]

        if not filtered_results:
            print("\nNo relevant documents found.")
            continue

        print("\nSearch result")

        for rank, (document, score) in enumerate(filtered_results, start=1):
            print(f"\nRank: {rank} | Similarity: {score:.4f}")
            print(document)


if __name__ == "__main__":
    main()
