import csv
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def load_txt(file_path):
    # Read txt file.
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found: {path}")

    text = path.read_text(encoding="utf-8")

    documents = []
    chunk_id = 0

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()  # remove blank

        if paragraph:  # only if paragraph contains an actual content
            # Append as a type of dictionary.
            document = {
                "text": paragraph,
                "source": path.name,
                "chunk_id": chunk_id,
            }

            documents.append(document)
            chunk_id += 1

    if not documents:
        raise ValueError(f"No text could be extracted from TXT: {path.name}")

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


def load_csv(file_path):
    # Read csv file.
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found: {path}")

    documents = []
    chunk_id = 0

    try:
        with path.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(
                    f"CSV header could not be found: {path.name}"
                )

            # The first line contains headers, so data starts from line 2.
            for row_number, row in enumerate(reader, start=2):
                row_texts = []

                for column, value in row.items():
                    if column is None or value is None:
                        continue

                    column = column.strip()
                    value = value.strip()

                    if column and value:
                        row_texts.append(f"{column}: {value}")

                if not row_texts:
                    continue

                text = "\n".join(row_texts)

                document = {
                    "text": text,
                    "source": path.name,
                    "chunk_id": chunk_id,
                    "row": row_number,
                }

                documents.append(document)
                chunk_id += 1

    except UnicodeDecodeError:
        raise ValueError(
            f"CSV must be saved with UTF-8 encoding: {path.name}"
        )

    except csv.Error as error:
        raise ValueError(
            f"CSV could not be parsed: {path.name} ({error})"
        )

    if not documents:
        raise ValueError(f"No data could be extracted from CSV: {path.name}")

    return documents


def is_url(source):
    parsed_url = urlparse(str(source))

    return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)


def load_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0/"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise ValueError(f"Web page could not be loaded: {url} ({error})")

    content_type = response.headers.get("Content-Type", "").lower()

    if "text/html" not in content_type:
        raise ValueError(f"URL does not contain an HTML page: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elements that do not contain the main page content.
    for tag in soup.find_all(
            ["script", "style", "nav", "footer", "header", "noscript"]
    ):
        tag.decompose()

    documents = []
    chunk_id = 0

    for element in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        text = element.get_text(" ", strip=True)

        if not text:
            continue

        document = {
            "text": text,
            "source": url,
            "chunk_id": chunk_id,
        }

        documents.append(document)
        chunk_id += 1

    if not documents:
        raise ValueError(f"No text could be extracted from URL: {url}")

    return documents


def load_document(source):
    # If the source is url.
    if is_url(source):
        return load_url(source)

    path = Path(source)

    if not path.exists():
        raise FileNotFoundError(f"File can't be found: {path}")

    extension = path.suffix.lower()

    # If the file is txt file.
    if extension == ".txt":
        return load_txt(path)

    # If the file is pdf file.
    if extension == ".pdf":
        return load_pdf(path)

    # If the file is csv file.
    if extension == ".csv":
        return load_csv(path)

    raise ValueError(f"Unsupported document type: {extension}")
