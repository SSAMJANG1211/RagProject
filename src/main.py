from pathlib import Path

from embedder import TextEmbedder
from document_loader import load_paragraphs
from prompt_builder import build_prompt
from retriever import FaissRetriever
from generator import AnswerGenerator


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "sample.txt"

    documents = load_paragraphs(data_path)

    print(f"{len(documents)} paragraphs loaded.")

    document_texts = []

    for document in documents:
        document_texts.append(document["text"])

    print("Loading embedding model...")
    embedder = TextEmbedder()
    print("Embedding model loaded.")

    print("Generating document embeddings...")
    document_embeddings = embedder.encode_documents(document_texts)
    print("Document embeddings generated.")

    print("Creating FAISS index...")

    retriever = FaissRetriever(
        document_embeddings,
        documents,
    )

    print("FAISS index created.")

    generator = AnswerGenerator()

    threshold = 0.1
    top_k = 3

    while True:
        query = input("\nEnter query(q to quit): ").strip()

        if query.lower() == "q":
            print("Program terminated.")
            break

        if not query:
            print("Please enter a query.")
            continue

        query_embedding = embedder.encode_query(query)

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

        prompt = build_prompt(query, filtered_results, )

        print("\nGenerating answer...")

        answer = generator.generate(prompt)

        print("\nGenerated answer")
        print(answer)


if __name__ == "__main__":
    main()
