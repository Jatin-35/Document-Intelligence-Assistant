import chromadb
from utils.logger import logger
import numpy as np

client = chromadb.Client()
collection = client.get_or_create_collection("document_chunks")

def store_chunks(chunks: list[str], embeddings: list, doc_id: str):
    try:
        if chunks is None or embeddings is None:
            raise ValueError("Chunks or embeddings are None.")
        if len(chunks) == 0 or len(embeddings) == 0:
            raise ValueError("Chunks or embeddings list is empty.")
        if len(chunks) != len(embeddings):
            raise ValueError("Mismatch between number of chunks and embeddings.")

        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            if embedding is None:
                raise ValueError(f"Embedding at index {idx} is None.")
            if hasattr(embedding, "__len__") and len(embedding) == 0:
                raise ValueError(f"Embedding at index {idx} is empty.")

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{doc_id}_{idx}"],
                metadatas=[{"doc_id": doc_id, "chunk_index": idx}]
            )

        logger.info(f"Successfully stored {len(chunks)} chunks for doc_id: {doc_id}")

    except Exception as e:
        logger.error(f"Error storing chunks in ChromaDB for doc_id={doc_id}: {e}")
