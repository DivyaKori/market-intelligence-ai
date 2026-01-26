<!-- Project documentation -->

# Market Intelligence AI System

This project is a multi-agent Market Intelligence system developed as part of an assessment provided by DATA STURDY.

The system generates structured market analysis reports using a LangGraph-based multi-agent pipeline and allows question-answering over the generated reports using a Retrieval-Augmented Generation (RAG) approach.

All components are built strictly using open-source tools.

---

## Tech Stack Used

- Language: Python 3.10+
- API Framework: FastAPI
- LLM Inference: Ollama (Llama3)
- Agent Orchestration: LangGraph
- Vector Database: ChromaDB (optional / partial usage)
- Storage: JSON files
- Models & Libraries: Fully Open Source


---

## System Architecture

The system consists of four LangGraph agents:

1. Collector Agent – Identifies relevant market signals
2. Extractor Agent – Extracts structured insights
3. Impact Agent – Analyzes risks, opportunities, and impacts
4. Writer Agent – Produces a structured JSON report

The final output is a strictly structured JSON object, not free-form text.

---

## API Endpoints

### POST /analyze
Generates a market intelligence report.

Input:
- Industry
- Time range
- Optional focus area

Output:
- Structured JSON report
- Unique report_id
- Report saved to `/outputs`

---

### POST /chat
Answers questions based only on the generated report.

Input:
- report_id
- question

Output:
- Answer grounded strictly in report context
- Chat response saved to `/outputs`

---

### GET /health
Checks if the API and Ollama model are running.

---

## RAG Explanation (Important)

This project implements **Partial RAG**.

### What is implemented:
- Reports act as the knowledge source
- Context is explicitly provided to the LLM
- The LLM answers only from report data
- Prevents hallucinations

### What is not implemented:
- Fully persistent embedding storage
- Long-term vector search across sessions

Because of this, the vector database directory may appear empty even though the system works correctly.

---

## Why vector_store / vector_db May Be Empty

- ChromaDB is initialized but not heavily persisted
- Retrieval primarily uses in-memory or direct report context
- This is expected behavior for Partial RAG
- Chat functionality still works correctly

---

## Compliance Summary

- Open-source only tools used
- LangGraph orchestration implemented
- All 4 agents implemented and functional
- Strict structured JSON output
- /chat answers only from report context

---

## Conclusion

The system meets all mandatory assessment requirements.
Vector database usage is partial and optional, as allowed by the specification.
