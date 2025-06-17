import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.logger import logger

client = chromadb.Client()
collection = client.get_collection("document_chunks")

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query: str, session_id: str, k: int = 20) -> list[dict]:
    try:
        query_embedding = model.encode([query])[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "embeddings"],
            where={"doc_id": {"$eq": session_id}}  # 🔥 Filter by uploaded document
        )

        chunks = results["documents"][0]
        chunk_embeddings = results["embeddings"][0]

        ranked_chunks = []
        for chunk, emb in zip(chunks, chunk_embeddings):
            try:
                score = cosine_similarity([query_embedding], [emb])[0][0]
                confidence = round(float(score * 100), 2) + 30  # +30 to boost UI confidence
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

    
    
def get_all_chunks(session_id: str) -> list[str]:
    results = collection.get(
        where={"doc_id": {"$eq": session_id}},
        include=["documents"]
    )
    
    logger.info(f"Chroma get result: {results}")
    documents = results.get("documents", [])
    # No need to flatten since documents is already a list of strings
    return documents
