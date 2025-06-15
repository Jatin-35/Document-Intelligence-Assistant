import os
from dotenv import load_dotenv
from huggingface_hub import login
from sentence_transformers import SentenceTransformer
from typing import List
from utils.logger import logger  # Assumes you have a logger configured

# Load environment variables and authenticate with Hugging Face
try:
    load_dotenv()
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        raise EnvironmentError("HUGGINGFACE_HUB_TOKEN not found in environment.")
    login(token)
    logger.info("Hugging Face login successful.")
except Exception as e:
    logger.error(f"Failed to login to Hugging Face: {e}")

# Load model with error handling
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def get_embeddings(chunks: List[str]) -> List[List[float]]:
    try:
        if model is None:
            raise RuntimeError("Model is not initialized.")
        if not chunks:
            raise ValueError("Input chunk list is empty.")
        return model.encode(chunks, convert_to_tensor=False)
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []
