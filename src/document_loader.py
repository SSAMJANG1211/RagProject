from pathlib import Path

from pypdf import PdfReader


def load_txt(file_path):
    # Read text file.
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


def load_pdf(file_path):
    # Read pdf file.
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found: {path}")

    reader = PdfReader(path)

    if reader.is_encrypted:  # does not support encrypted pdf file
        raise ValueError(f"Encrypted PDF is not supported: {path.name}")

    documents = []
    chunk_id = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text:
            continue

        text = text.strip()

        if text:  # only if text contains an actual content
            # Append as a type of dictionary.
            document = {
                "text": text,
                "source": path.name,
                "chunk_id": chunk_id,
                "page": page_number,
            }

            documents.append(document)
            chunk_id += 1

    if not documents:
        raise ValueError(f"No text could be extracted from PDF: {path.name}")

    return documents


def load_document(source):
    path = Path(source)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found. : {path}")

    extension = path.suffix.lower()

    # If the file is txt file.
    if extension == ".txt":
        return load_txt(path)

    # If the file is pdf file.
    if extension == ".pdf":
        return load_pdf(path)

    raise ValueError(f"Unsupported document type: {extension}")
