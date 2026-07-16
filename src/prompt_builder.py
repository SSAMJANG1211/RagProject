def build_prompt(query, search_results):
    context = ""

    for result in search_results:
        source = result["source"]
        chunk_id = result["chunk_id"]
        text = result["text"]

        context += f"[Source: {source}, Chunk: {chunk_id}]\n"
        context += text
        context += "\n\n"

    prompt = f"""
You are a question-answering assistant.

Answer the question using only the provided context.
If the context does not contain enough information,
say that you cannot find the answer in the document.
Do not make up information.

Context:
{context}

Question:
{query}

Answer:
""".strip()

    return prompt  # prompt that contains context and query
