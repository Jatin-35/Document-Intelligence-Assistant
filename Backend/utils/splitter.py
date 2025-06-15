from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logger import logger  # Assuming you're using a logger

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    try:
        if not text.strip():
            raise ValueError("Empty text provided for splitting.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )

        chunks = splitter.split_text(text)
        if not chunks:
            raise ValueError("Text splitting returned no chunks.")

        return chunks

    except Exception as e:
        logger.error(f"Error splitting text into chunks: {e}")
        return []
