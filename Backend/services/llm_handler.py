import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq
from utils.logger import logger
import time

load_dotenv()



def ask_llm(prompt: str) -> str:
    try:
        logger.info("Trying Groq API...")
        start = time.time()
        response = ask_groq(prompt)
        if time.time() - start > 2:  # If Groq takes more than 5 seconds
            raise Exception("GroqTooSlow")
        return response
    except Exception as e:
        logger.warning(f"Groq failed or was too slow: {e}")
        try:
            logger.info("Falling back to OpenRouter...")
            return ask_openrouter(prompt)
        except Exception as ex:
            logger.error(f"OpenRouter failed too: {ex}")
            return "Error: Both LLM APIs failed."



def ask_groq(prompt: str) -> str:
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not found in environment.")

        client = Groq(api_key=api_key)
        logger.info("Calling Groq with model: llama3-70b-8192")

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama3-70b-8192",
            stream=False
        )

        logger.info("Groq response received")
        return chat_completion.choices[0].message.content

    except Exception as e:
        # Detect rate limit or throttle response
        if hasattr(e, "status_code") and e.status_code == 429:
            logger.warning("Groq rate limit hit (429) — skipping retry and triggering fallback.")
            raise Exception("RateLimited")  # Custom trigger for fallback
        if "Too Many Requests" in str(e):
            logger.warning("Groq returned 'Too Many Requests' — triggering fallback.")
            raise Exception("RateLimited")
        logger.error(f"Groq error: {str(e)}")
        raise e


def ask_openrouter(prompt: str) -> str:
    try:
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not OPENROUTER_API_KEY:
            raise EnvironmentError("OPENROUTER_API_KEY not found in environment.")

        logger.info("Sending chat completion request to OpenRouter (gpt-4o-mini)")
        res = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions", 
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        response = res.json()
        if "choices" in response:
            logger.info("OpenRouter response received successfully")
            return response["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"OpenRouter response error: {response}")

    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        raise e



def build_prompt(context_chunks: list[str], question: str, memory: str = "") -> str:
    try:
        context = "\n\n".join(context_chunks)

        if not context.strip():
            raise ValueError("Context is empty, cannot build prompt.")
        if not question.strip():
            raise ValueError("Question is empty, cannot build prompt.")

        prompt = (
            "You are a helpful document assistant. Answer the user's question using the context below.\n\n"
            f"Context:\n{context}\n\n"
        )

        if memory.strip():
            prompt += f"Prior Conversation:\n{memory}\n\n"

        prompt += (
            f"Current Question:\n{question}\n\n"
            "You may synthesize answers from context, memory, or both. Even if the exact term is not used (e.g. 'school'), use the meaning to answer correctly."
            "Even if the exact answer isn't found, try your best based on the available information."
        )

        return prompt

    except Exception as e:
        logger.error(f"Error building prompt: {e}")
        return "Error: Could not build prompt."



