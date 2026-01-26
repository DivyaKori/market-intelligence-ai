# Market Intelligence AI – Run Guide & Usage

This document explains how to set up, run, and use the **Market Intelligence AI** project locally.

---

## 1. Project Overview

This project is a **multi-agent market intelligence system** built using:

- **FastAPI** for APIs
- **LangGraph** for agent orchestration
- **Ollama (Llama3)** for LLM inference
- **ChromaDB** (optional) for vector-based retrieval
- **Python 3.10+**

### Current Capabilities
- Generates structured market reports via `/analyze`
- Saves reports as JSON
- Allows Q&A over generated reports via `/chat`
- Uses report content as context (partial RAG behavior)

---

## 2. Prerequisites

Make sure you have:

- Python **3.10+**
- **Ollama** installed and working
- Git (optional)

Verify Python:
```bash
python --version

## 3. Create Virtual Environment and Activate it
From the project root directory:

python -m venv venv
venv\Scripts\activate

## 4. Install Dependencies
pip install -r requirements.txt

## 5. Start Ollama Model
Run the LLM locally:

ollama run llama3


⚠️ Important:
Keep this running in the background while using the application.

## 6. Run the FastAPI Server
Open a new terminal (with venv activated):

uvicorn app:app --reload


If successful, you will see:

Uvicorn running on http://127.0.0.1:8000

## 7. Open API Documentation (Swagger UI)

Open your browser and go to:

http://127.0.0.1:8000/docs


Use Swagger UI to test all endpoints.

## 8. API Usage Examples
### 8.1 /analyze – Generate Market Report

Endpoint

POST /analyze


Request Body

{
  "industry": "Fintech",
  "from_date": "2023-01-01",
  "to_date": "2024-01-01",
  "focus": "regulatory changes in India"
}


What happens

LangGraph agents generate a structured market report

Report is saved as a JSON file

A report_id is returned for chat usage

### 8.2 /chat – Ask Questions on Generated Report

Endpoint

POST /chat


Request Body

{
  "report_id": "YYYYMMDD_HHMMSS",
  "question": "What are the key risks mentioned?"
}


What happens

Relevant report content is used as context

LLM answers strictly based on the report

Chat output is saved as a JSON file
