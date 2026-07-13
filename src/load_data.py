from pathlib import Path

def load_paragraphs(file_path: str) -> list[str]:
    """Read text file and split paragraphs by empty line."""
    path = Path(file_path);

    if not path.exists():
        raise FileNotFoundError(f"File can't be found. : {path}")

    text = path.read_text(encoding="utf-8")

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    return paragraphs