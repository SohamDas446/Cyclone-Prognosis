from pathlib import Path
import json

from sentence_transformers import SentenceTransformer
import numpy as np


KNOWLEDGE_DIR = Path("data/knowledge")
VECTOR_STORE_DIR = Path("data/vector_store")
VECTOR_STORE_FILE = VECTOR_STORE_DIR / "knowledge_base.json"

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def chunk_text(text: str, chunk_size: int = 80):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def build_knowledge_base():
    documents = []

    for document in load_documents():

        chunks = chunk_text(document["text"])

        for chunk in chunks:

            embedding = model.encode(chunk)

            documents.append({
                "source": document["source"],
                "text": chunk,
                "embedding": embedding.tolist()
            })

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file)

    return documents


def load_knowledge_base():

    if not VECTOR_STORE_FILE.exists():
        return build_knowledge_base()

    with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_knowledge(query: str, top_k: int = 3):

    documents = load_knowledge_base()

    query_embedding = model.encode(query)

    scores = []

    for document in documents:

        document_embedding = np.array(
            document["embedding"]
        )

        similarity = np.dot(
            query_embedding,
            document_embedding
        ) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(document_embedding)
        )

        scores.append({
            "source": document["source"],
            "text": document["text"],
            "score": float(similarity)
        })

    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scores[:top_k]