from pathlib import Path

from embed import TextEmbedder
from load_data import load_paragraphs
from search import search_top_k


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "sample.txt"

    documents = load_paragraphs(data_path)

    print(f"{len(documents)} paragraphs loaded.")

    print("Loading embedding model...")
    embedder = TextEmbedder()
    print("Embedding model loaded.")

    print("Generating document embeddings...")
    document_embeddings = embedder.encode_documents(documents)
    print("Document embeddings generated.")

    threshold = 0.3

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
            query_embedding,
            document_embeddings,
            documents,
            3,
        )

        filtered_results = []
        for document, score in results:
            if score >= threshold:
                filtered_results.append((document, score))

        if (filtered_results) == 0:
            print("\nNo relevant documents found.")
            continue

        print("\nSearch result")

        rank = 1
        for document, score in filtered_results:
            print(f"\nRank: {rank} | Similarity: {score:.4f}")
            print(document)

            rank += 1


if __name__ == "__main__":
    main()
