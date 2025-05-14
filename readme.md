# Project Proposal Assistant (Hobglobin Take-Home Assignment)

This is a lightweight, production-style MVP designed to help users **generate project proposal summaries** and **interactively query PDF documents** using a Retrieval-Augmented Generation (RAG) pipeline powered by the **Gemini API**.

---

## 🚀 Features

- 📄 Extracts "fine-prints" — key project details — from PDFs.
- 💬 Provides a chatbot interface for querying documents contextually.
- ⚡ Built with FastAPI, LangChain, and Gemini for rapid and smart document analysis.
- 🖥️ Clean, responsive HTML interface using vanilla HTML/CSS.


## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
# Clone this repo (if applicable)
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create a Virtual Environment
```bash
conda create -n proposal-assistant python=3.10 -y
conda activate proposal-assistant
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Gemini API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> 🔐 **Never commit your `.env` or API keys to source control.**

### 5. Run the App
```bash
uvicorn main:app --reload
```

### 6. Access the App
- Main UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 API Endpoints

### `GET /fine-prints`
Returns extracted fine-print summary from documents.

### `POST /chat`
Accepts a JSON query and returns contextual response.
```json
{
  "query": "What is the project scope?"
}
```

---

## Submission Files

- `chat_response.txt` — Responses to sample questions using `/chat`
- `fine_prints.txt` — Output from `/fine-prints` endpoint

---

## ✨ Highlights

- Well-structured modular code using FastAPI, LangChain, Gemini, and FAISS.
- Clean separation of frontend and backend logic.
- Clear, polished user interface designed to be intuitive and responsive.
- Secure and scalable API-first approach.

---

## Possible Extensions

- Upload PDF support (currently loads from `/data/` folder)
- Chat history persistence
- File-specific query context
- Support for additional file formats (e.g., DOCX, TXT)

---

## Author
Built by Nairutya Patel as part of the Hobglobin AI take-home assessment.

---
