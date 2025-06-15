import pdfplumber
import docx
from typing import Union
import os
from utils.logger import logger  # assuming you have a logger set up

def extract_text(file_path: str, file_type: str) -> str:
    text = ""

    try:
        if file_type == "pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        elif file_type == "docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif file_type == "txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text += f.read()

        else:
            raise ValueError("Unsupported file type")

        if not text.strip():
            raise ValueError("No text extracted from document.")

        return text.strip()

    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return ""
