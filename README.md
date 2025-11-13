# 📄 Document Intelligence Assistant

A smart web-based assistant that allows users to upload documents (`PDF`, `DOCX`, `TXT`), ask questions, and get meaningful answers or summaries using modern AI models and semantic search.

---

## 📁 Folder Structure

### 🧠 Backend Folder Structure (/Backend) 
``` 
Backend/
├── api/
│   └── routes.py                    # FastAPI route definitions (upload, ask, summarize, reset)
│
├── db/ 
│   └── chroma_store.py              # ChromaDB vector store setup and operations
│
├── services/
│   ├── document_handler.py         # File parsing (PDF, DOCX, TXT)
│   ├── embedder.py                 # Embedding generation using sentence-transformers
│   ├── llm_handler.py              # LLM calling logic (Groq/OpenRouter fallback)
│   ├── pipeline.py                 # Core ingestion & chunking pipeline
│   └── retriever.py                # Semantic search (retrieves relevant document chunks)
│
├── temp_uploads/                   # Temporary file storage during upload
│   ├── Edusphere paper.pdf
│   ├── Honors Final Assessment.docx
│   └── ...
│
├── utils/
│   ├── answer_modifier.py         # Format and clean LLM responses
│   ├── logger.py                  # Structured logging configuration
│   ├── memory_json.py            # Store/retrieve Q&A memory per session in JSON
│   └── splitter.py               # Chunking logic for large text
│
├── conversation_memory.json       # Stores conversation history for sessions
├── main.py                        # FastAPI entrypoint and route registration
├── app.log                        # Log file for backend operations
├── .env                           # Backend environment variables
├── .gitignore                     # Ignore unnecessary files in Git
└── requirements.txt               # Python dependencies

```

### 💻 Frontend Folder Structure (/Frontend)

```
Frontend/
├── app/
│   ├── layout.tsx                     # Shared layout for all pages
│   └── page.tsx                       # Main document assistant interface
│
├── components/
│   ├── ui/                            # Reusable UI primitives
│   │   ├── alert.tsx
│   │   ├── badge.tsx
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── separator.tsx
│   │
│   ├── document-upload.tsx           # File upload component
│   ├── question-form.tsx             # Input box for asking questions
│   ├── reset-memory-button.tsx       # Button to clear session memory
│   ├── response-display.tsx          # Shows assistant's response
│   └── summarize-button.tsx          # Button to trigger document summarization
│
├── hooks/
│   └── use-document-assistant.ts     # Custom hook managing document assistant logic
│
├── lib/
│   ├── api.ts                         # API interaction functions (ask, upload, summarize)
│   ├── types.ts                       # TypeScript types and interfaces
│   └── utils.ts                       # Utility helpers
│
├── src/styles/
│   └── globals.css                    # Tailwind base styles and global CSS
│
├── .env.example                       # Example environment config
├── .env.local                         # Local environment config
├── .gitignore                         # Git ignored files
├── components.json                    # Shadcn UI config (if used)
├── next-env.d.ts                      # TypeScript declaration for Next.js
├── package.json                       # Project config and dependencies
├── package-lock.json                  # Lockfile for reproducible installs
├── postcss.config.js                  # PostCSS config
├── tailwind.config.js                 # Tailwind CSS config
└── tsconfig.json                      # TypeScript compiler options

```
---

## 🚀 Features

- 📤 Upload support for PDF, DOCX, and TXT
- 🔍 Semantic search over document content using embeddings
- 💬 Ask questions and receive contextual, accurate answers
- 🧠 Maintains conversation memory per document session
- 🧾 Summarization in clean markdown bullet-point format
- 🔄 API fallback support (Groq → OpenRouter)

---

## 🛠️ Tech Stack

| Layer         | Tech                                                                 |
|---------------|----------------------------------------------------------------------|
| Frontend      | React + Tailwind (Next.js)                                    |
| Backend       | Python + FastAPI                                                     |
| Embeddings    | `sentence-transformers/all-MiniLM-L6-v2` or `hkunlp/instructor-xl`   |
| Vector Store  | Chroma DB                                                            |
| LLMs          | Groq (`llama3-70b-8192`), OpenRouter (`gpt-4o-mini`)                 |
| File Parsing  | `pdfplumber`, `python-docx`                                          |

---

## 📦 Setup Instructions

### Backend Setup (FastAPI + ChromaDB + LLM APIs)

```bash
# Step 0: Cloning instructions
git clone https://github.com/Jatin-35/Document-Intelligence-Assistant.git
cd Document-Intelligence-Assistant

# Step 1: Create a virtual environment using UV (faster than pip)
uv venv .venv

# Step 2: Activate the virtual environment
# On Unix or MacOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Step 3: Install Python dependencies listed in requirements.txt
uv pip install -r requirements.txt

# Step 4: Set up environment variables (copy the example and add your keys)
 .env

# Open the .env file and add:
# GROQ_API_KEY=your_groq_key
# OPENROUTER_API_KEY=your_openrouter_key

# Step 5: Run the FastAPI server in development mode
uvicorn main:app --reload
```
- Dependencies: fastapi, uvicorn, sentence-transformers, chromadb, pdfplumber, python-docx, and others.

### 💻 Frontend

```bash
# Step 1: Move into the frontend directory
cd frontend

# Step 2: Install all frontend dependencies
npm install

# Step 3: Run the frontend development server
npm run dev

# Step 4 (only if setting up fresh from scratch):

# 4.1 - Install Tailwind CSS & its dependencies
npx tailwindcss init -p

# 4.2 - Add global styles and content paths
# In tailwind.config.js:
# content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"]

# 4.3 - Initialize shadcn/ui
npx shadcn-ui@latest init

# Follow prompts and select:
# > App directory: yes
# > Typescript: yes
# > Tailwind CSS: yes
# > Component path: ./components/ui

# 4.4 - Install any specific component (e.g. Button)
npx shadcn-ui@latest add button
```
 - Libraries used: next, tailwindcss, shadcn/ui, lucide-react, clsx, and other TypeScript utilities.

---
## ✅ Dataset Information

This project does not rely on any external or pre-built datasets. All data is provided dynamically by users at runtime when they upload their documents. The system processes documents in **PDF, DOCX, and TXT** formats.

### **Source of Data**
- Documents are uploaded by users through the web interface.
- Files are stored temporarily in the directory:  
  **`/Backend/temp_uploads/`**
- No document is permanently stored unless explicitly chosen by the user.


### **Data Size**
- File size varies depending on user uploads.
- The system is optimized to handle both small and large documents using chunking and semantic indexing.

---

## 🧾 **Preprocessing Steps Applied**
Each uploaded document follows a structured preprocessing pipeline:

#### **1. Text Extraction**
- `pdfplumber` for PDF parsing  
- `python-docx` for DOCX parsing  
- Standard text loaders for TXT files  

#### **2. Cleaning & Normalization**
- Removal of special characters  
- Standardization of whitespace  
- Basic text normalization to improve chunk quality  

#### **3. Chunking into Semantic Units**
- Document split into meaningful segments  
- Overlapping window strategy to maintain context  
- Chunk sizes tuned for efficient retrieval and LLM constraints  

#### **4. Embedding Generation**
Embeddings generated via one of the following:
- `sentence-transformers/all-MiniLM-L6-v2`
- `hkunlp/instructor-xl` (optional for higher accuracy)

#### **5. Vector Indexing**
- Chunks are stored in a **ChromaDB** collection  
- Metadata stored with each entry:
  - `doc_id`
  - `session_id`

This preprocessing pipeline ensures high-quality semantic search, accurate retrieval, and grounded responses formatted by the LLM.

<img width="546" height="742" alt="image" src="https://github.com/user-attachments/assets/87350c20-4288-44e5-a531-eb43cde42791" />

---

## Architecture Flow Diagram

<img width="600" height="600" alt="📄 Document Intelligence Assistant - visual selection (1)" src="https://github.com/user-attachments/assets/eb5b1c16-18b3-4b7e-9c79-d83d88380b80" />

> “This flow diagram shows how the Document Intelligence Assistant processes uploaded documents through splitting, embedding, retrieval, and LLM reasoning to generate accurate, context-grounded answers.”
---
## 🧪 Usage

1. Open the web interface.
2. Upload a supported document (`PDF`, `DOCX`, or `TXT`).
3. Ask natural language questions like:
   - “What is this document about?”
   - “Summarize the key points.”
4. View highlighted document chunks with confident LLM-generated answers.
5. Click **📄 Summarize Document** to generate a clean bullet-point summary.


Below is an example illustrating how the Document Intelligence Assistant processes a document, understands a user query, and generates grounded, context-aware responses.

---

### 📘 Sample Input Document

**File:** *“AI in Healthcare.pdf”*

**Content (excerpt):**
> “Although AI is transforming medical diagnostics, several challenges remain, including regulatory compliance, patient data privacy, limited availability of annotated medical datasets, and the high computational resources required for training large models.”

### ❓ Sample User Query

What are the main challenges mentioned?

### ✅ Expected Output

Based on semantic retrieval of the most relevant chunks and LLM-based reasoning, the system would generate a structured answer similar to the following:

#### **Answer**
The document highlights several key challenges associated with the use of AI in healthcare:

- **Regulatory compliance issues**  
- **Data privacy and protection concerns**  
- **Limited availability of high-quality, annotated medical datasets**  
- **High computational costs** for training and deploying advanced AI models  

### 🧩 Supporting Evidence (Retrieved Chunks)

The assistant also returns the document segments used to answer the query, along with the confidence score:


---

## 🌟 Advanced Features

- **API Integration (Fallback)** – Automatically switches from Groq to OpenRouter when rate-limited (HTTP 429).
- **Conversation Memory** – Maintains Q&A history per document session to preserve context and improve relevance.
- **Summarization** – Converts raw document content into clean, markdown-formatted bullet points using LLMs.

---

👨‍💻 Author
Developed  by [Jatin Jasrotia](https://github.com/Jatin-35), Ankitkumar Patel, Madhav Gupta



