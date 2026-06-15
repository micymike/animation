"""Build the vector index from the Finance Bill PDF."""
import sys
from pathlib import Path

from rag import build_index

PDF_PATH = Path(__file__).parent / "Finance_Bill_2026_text.pdf"

if __name__ == "__main__":
    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    force = "--force" in sys.argv
    build_index(str(PDF_PATH), force_rebuild=force)
    print("Done. Index is ready.")
