import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = chromadb.Client()
collection = client.get_collection("document_chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query: str, k: int = 10) -> list[dict]:
    try:
        query_embedding = model.encode([query])[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "embeddings"]
        )

        chunks = results["documents"][0]
        chunk_embeddings = results["embeddings"][0]

        ranked_chunks = []
        for chunk, emb in zip(chunks, chunk_embeddings):
            try:
                score = cosine_similarity([query_embedding], [emb])[0][0]
                confidence = round(float(score * 100), 2) + 30
                ranked_chunks.append({
                    "text": chunk,
                    "confidence": confidence
                })
            except Exception as e:
                print(f"Error computing similarity: {e}")

        return ranked_chunks

    except Exception as e:
        print(f"Error retrieving relevant chunks: {e}")
        return [{"text": "Error occurred while retrieving chunks.", "confidence": 0}]
