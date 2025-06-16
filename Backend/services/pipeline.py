from services.document_handler import extract_text
from utils.splitter import chunk_text
from services.embedder import get_embeddings
from db.chroma_store import store_chunks
import uuid

def process_document(file_path: str, file_type: str , session_id : str):
    try:
        

        text = extract_text(file_path, file_type)
        if not text:
            raise ValueError("No text extracted from the document.")

        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("Text could not be split into chunks.")

        embeddings = get_embeddings(chunks)
        if embeddings is None or len(embeddings) != len(chunks):
            raise ValueError("Embedding generation failed or mismatched with chunks.")

        store_chunks(chunks, embeddings, session_id)

        return {
            "doc_id": session_id,
            "num_chunks": len(chunks)
        }

    except Exception as e:
        print(f"[process_document] Error: {e}")
        return {
            "error": str(e),
            "doc_id": None,
            "num_chunks": 0
        }
