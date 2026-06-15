import os
import json
import pickle
import hashlib
import re
from pathlib import Path
from typing import Optional

import pdfplumber
import numpy as np
from tiktoken import encoding_for_model
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384
CHUNK_SIZE = 600
CHUNK_OVERLAP = 120
INDEX_DIR = Path(__file__).parent / ".rag_index"
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"
CHUNKS_FILE = INDEX_DIR / "chunks.pkl"

_enc = encoding_for_model("gpt-3.5-turbo")
_embedder = None


def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL, truncate_dim=512)
    return _embedder


def _local_embed(texts: list[str]) -> np.ndarray:
    embedder = _get_embedder()
    return embedder.encode(texts, normalize_embeddings=True, show_progress_bar=False)


def _num_tokens(text: str) -> int:
    return len(_enc.encode(text))


def extract_text(pdf_path: str) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def chunk_text(text: str) -> list[dict]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    buffer = ""
    buffer_tokens = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_tokens = _num_tokens(para)
        if buffer_tokens + para_tokens > CHUNK_SIZE and buffer:
            chunks.append({"text": buffer.strip(), "tokens": buffer_tokens})
            overlap_text = buffer.split(". ")[-3:] if ". " in buffer else [buffer[-200:]]
            buffer = ". ".join(overlap_text) + ". " if isinstance(overlap_text, list) else buffer[-200:]
            buffer_tokens = _num_tokens(buffer)
        buffer += ("\n\n" if buffer else "") + para
        buffer_tokens = _num_tokens(buffer)

    if buffer.strip():
        chunks.append({"text": buffer.strip(), "tokens": buffer_tokens})
    return chunks


def build_index(pdf_path: str, force_rebuild=False):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    if EMBEDDINGS_FILE.exists() and not force_rebuild:
        return load_index()

    print(f"Extracting text from {pdf_path}...")
    text = extract_text(pdf_path)
    print(f"Extracted {_num_tokens(text)} tokens")

    print("Chunking...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    print("Embedding...")
    texts = [c["text"] for c in chunks]
    all_embeddings = []
    batch_size = 16
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"  Batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1} ({len(batch)} texts)")
        emb = _local_embed(batch)
        all_embeddings.append(emb)

    embeddings = np.concatenate(all_embeddings, axis=0).astype("float32")
    print(f"Embedding shape: {embeddings.shape}")

    np.save(str(EMBEDDINGS_FILE), embeddings)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Index saved to {EMBEDDINGS_FILE}")

    return embeddings, chunks


def load_index():
    if not EMBEDDINGS_FILE.exists():
        return None, None
    embeddings = np.load(str(EMBEDDINGS_FILE))
    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)
    return embeddings, chunks


def search(query: str, k: int = 5) -> list[dict]:
    embeddings, chunks = load_index()
    if embeddings is None:
        return [{"text": "No index found. Run build_index() first.", "score": 0, "source": "system"}]

    query_vec = _local_embed([query]).astype("float32")
    similarities = np.dot(embeddings, query_vec.T).flatten()
    top_k = np.argsort(similarities)[::-1][:k]

    results = []
    for idx in top_k:
        score = float(similarities[idx])
        if idx < len(chunks) and score > 0.3:
            results.append({
                "text": chunks[idx]["text"],
                "score": score,
                "source": f"Chunk {idx + 1}",
            })
    return results
