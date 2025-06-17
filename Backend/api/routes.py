import os
import json
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from services.pipeline import process_document
from services.retriever import retrieve_relevant_chunks , get_all_chunks
from services.llm_handler import ask_llm, build_prompt
from utils.logger import logger  
from utils.memory_json import add_to_memory, get_memory , load_memory , save_memory
from utils.answer_modifier import format_summary
from db.chroma_store import store_summary
import uuid


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
        doc_id = str(uuid.uuid4())
        result = process_document(file_path, file_type , session_id = doc_id)

        if "error" in result:
            raise ValueError(result["error"])

        return {
            "status": "success",
            "file": file.filename,
            "filetype": file_type,
            "doc_id" : result["doc_id"],
            "chunks": result["num_chunks"]
        }

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/ask")
async def ask_question(
    question: str = Form(...),
    session_id: str = Form(...)
):
    try:
        logger.info(f"Received question from session: {session_id}")

        # Step 1: Retrieve top relevant chunks
        chunks = retrieve_relevant_chunks(question , session_id=session_id)

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


@router.post("/summarize")
async def summarize_document(session_id: str = Form(...)):
    try:
        chunks = get_all_chunks(session_id=session_id)
        if not chunks:
            return {"summary": "No document chunks available to summarize."}

        # 🔍 Filter out small or meaningless chunks
        MIN_CHUNK_LENGTH = 50
        chunk_limit = min(len(chunks), 10)
        meaningful_chunks = [c for c in chunks if len(c.strip()) > MIN_CHUNK_LENGTH][:chunk_limit]

        if not meaningful_chunks:
            return {"summary": "The document does not contain enough meaningful content to summarize."}

        joined_context = "\n\n".join(meaningful_chunks)

        # 🧠 Dynamic prompt construction
        if len(meaningful_chunks) < 5:
            prompt = (
                "The document contains limited content. Summarize it into clear, well-structured markdown bullet points:\n"
                "- Use `- **Title**: description` format where applicable.\n\n"
                f"{joined_context}"
            )
        else:
            prompt = (
                "You are an expert technical writer. Summarize the following document using exactly 7 clear, concise, and well-formatted bullet points.\n\n"
                f"{joined_context}\n\n"
                "📝 Instructions:\n"
                "- Do not include any introductory sentences like 'Here's the summary'.\n"
                "- Format each bullet using Markdown as: `- **Title**: Description...`\n"
                "- Emphasize the document's **purpose**, **problem**, **key contributions**, **methods**, **features**, **impact**, and **conclusion**.\n"
                "- Avoid casual tone, opinions, or unnecessary filler. Just informative points.\n"
                "- Begin immediately with the first bullet point."
            )

        # 🔁 Ask the LLM
        summary = ask_llm(prompt).strip().lstrip("Summary:").strip()

        # 💾 Store summary for reuse
        store_summary(session_id, summary)

        return {"summary": summary}

    except Exception as e:
        logger.error(f"Summarization failed for session_id={session_id}: {e}")
        logger.debug(f"Chunks: {chunks}")
        raise HTTPException(status_code=500, detail="Failed to summarize document.")


     
    
# @router.post("/reset_memory")
# async def reset_memory(session_id: str = Form(...)):
#     memory = load_memory()
#     if session_id in memory:
#         del memory[session_id]
#         save_memory(memory)
#         return JSONResponse(content={"status": "Memory cleared."}, status_code=200)
#     else:
#         return JSONResponse(content={"status": "No memory found for session."}, status_code=404)
