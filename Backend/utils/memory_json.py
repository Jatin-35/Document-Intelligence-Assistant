import json
import os

MEMORY_FILE = "conversation_memory.json"

# Load memory from file
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

# Add a new user-assistant pair
def add_to_memory(session_id: str, question: str, answer: str):
    memory = load_memory()
    if session_id not in memory:
        memory[session_id] = []
    memory[session_id].append({
        "user": question,
        "assistant": answer
    })
    save_memory(memory)

# Get last n Q&A pairs as formatted string for context
def get_memory(session_id: str, limit: int = 2) -> str:
    memory = load_memory()
    if session_id not in memory:
        return ""
    history = memory[session_id][-limit:]
    return "\n\n".join([
        f"User: {entry['user']}\nAssistant: {entry['assistant']}" for entry in history
    ])
