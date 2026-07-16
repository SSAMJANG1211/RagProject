from pathlib import Path


def load_paragraphs(file_path):
    # Read text file and split paragraphs by empty line.
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found. : {path}")

    text = path.read_text(encoding="utf-8")

    documents = []
    chunk_id = 0
    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()  # remove blank

        if paragraph:  # only if paragraph contains an actual content (not blank)
            # Append as a type of dictionary.
            document = {
                "text": paragraph,
                "source": path.name,
                "chunk_id": chunk_id,
            }

            documents.append(document)
            chunk_id += 1

    return documents
