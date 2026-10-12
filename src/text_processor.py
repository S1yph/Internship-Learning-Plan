from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parent.parent
data_dir = ROOT / "data"
output_PATH = ROOT / "output" / "documents.json"

def load_documents(data_dir) -> list[dict]:
        documents = []
        for i, path in enumerate(sorted(Path(data_dir).glob("*.txt")), start=1):
            documents.append(
                {
                    "id": f"doc_{i:03d}",
                    "filename": path.name,
                    "text": path.read_text(encoding="utf-8"),
                }
            )
        return documents


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r","\n")
    lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in text.split("\n")
    ]
    return "\n".join(line for line in lines if line)

def chunk_text(text: str, chunk_size: int = 10) -> list[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

def process_document(doc: dict, chunk_size: int = 10) -> dict:
    text = clean_text(doc["text"])
    chunks = chunk_text(text)
    return {
        "id": doc["id"],
        "filename": doc["filename"],
        "text": text,
        "character_count": len(text),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }

def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True) #若目录存在，不报错
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii= False, indent = 2)

def print_summary(documents: list[dict]) -> None:
    n_docs = len(documents)
    n_chars = sum(d["character_count"] for d in documents)
    n_chunks = sum(d["chunk_count"] for d in documents)
    avg = n_chars / n_docs if n_docs else 0.0
    print(f"Documents: {n_docs}")
    print(f"Characters: {n_chars}")
    print(f"Chunks: {n_chunks}")
    print(f"Average document length: {avg:.1f}")
 
def main() -> None:
    raw_docs = load_documents(data_dir)
    processed = [process_document(d) for d in raw_docs]
    save_json(processed, output_PATH)
    print_summary(processed)
    print(f"Saved to {output_PATH}")
    
if __name__ == "__main__":
    main()
