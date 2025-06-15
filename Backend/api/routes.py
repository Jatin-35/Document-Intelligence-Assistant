import os
import json
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from services.pipeline import process_document
from services.retriever import retrieve_relevant_chunks
from services.llm_handler import ask_llm, build_prompt
from utils.logger import logger  
from utils.memory_json import add_to_memory, get_memory , load_memory , save_memory


router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        upload_dir = "temp_uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        file_type = file.filename.split(".")[-1].lower()
        result = process_document(file_path, file_type)

        if "error" in result:
            raise ValueError(result["error"])

        return {
            "status": "success",
            "file": file.filename,
            "filetype": file_type,
            "chunks": result["num_chunks"]
        }

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/ask")
async def ask_question(
    question: str = Form(...),
    session_id: str = Form(default="default")
):
    try:
        logger.info(f"Received question from session: {session_id}")

        # Step 1: Retrieve top relevant chunks
        chunks = retrieve_relevant_chunks(question)

        # 🧪 Log chunks for debugging
        logger.info("Chunks passed to LLM:")
        for i, chunk in enumerate(chunks):
            logger.info(f"Chunk {i+1} (Confidence {chunk['confidence']}%):\n{chunk['text']}\n")

        # Step 2: Get conversation memory
        memory = get_memory(session_id)

        # Step 3: Build prompt with memory + context
        prompt = build_prompt([chunk["text"] for chunk in chunks], question, memory)
        logger.info(f"Prompt being sent to LLM:\n{prompt}")

        # Step 4: Get answer from LLM
        answer = ask_llm(prompt)

        # Step 5: Update memory
        add_to_memory(session_id, question, answer)

        logger.info("Question answered successfully")

        return {
            "session": session_id,
            "question": question,
            "answer": answer,
            "sources": chunks
        }

    except Exception as e:
        logger.error(f"Question answering failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")



@router.get("/summarize")
async def summarize():
    try:
        # Placeholder: Replace with real summarization logic
        return {"summary": "This will be your document summary."}
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to summarize document.")
    
    
@router.post("/reset_memory")
async def reset_memory(session_id: str = Form(...)):
    memory = load_memory()
    if session_id in memory:
        del memory[session_id]
        save_memory(memory)
        return JSONResponse(content={"status": "Memory cleared."}, status_code=200)
    else:
        return JSONResponse(content={"status": "No memory found for session."}, status_code=404)
