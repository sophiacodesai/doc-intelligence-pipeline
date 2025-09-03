# Document Intelligence Pipeline

This repository compares two intelligent approaches for parsing documents:

1. **Azure Document Intelligence – prebuilt structured models**  
   → e.g. invoice extraction using `prebuilt-invoice`
2. **OCR-based layout parsing with GPT post-processing**  
   → e.g. LLM extracting fields from scanned/unstructured PDFs

---

## Why This Project?

In practice, businesses deal with both structured (invoices, paystubs) and unstructured documents (scans, inconsistent templates).  
This pipeline helps answer a critical question:

> **When is it better to use a prebuilt model vs a GPT-based parser?**

It’s ideal for:
- Companies automating document workflows
- Teams evaluating trade-offs between structure vs flexibility
- Developers comparing classic vs generative approaches

---

## Features

- ✅ Invoice parsing via `prebuilt-invoice`
- ✅ Pay stub parsing (optional via `prebuilt-payStub.us`)
- ✅ OCR-based layout extraction (Azure `prebuilt-layout`)
- ✅ GPT-based structured parsing from layout
- ✅ REST API using FastAPI
- ✅ Supports both classic and LLM-based document extraction


---

## API Overview

This FastAPI-based backend provides the following REST endpoints:

| Endpoint                 | Description                                     |
|--------------------------|-------------------------------------------------|
| `GET /health`            | Health check                                   |
| `POST /extract/invoice`  | Extract structured invoice data                |
| `POST /extract/ocr-llm`  | Extract via OCR + GPT (free-text instructions) |

---

## Example Architecture

```text
┌───────────────┐       ┌────────────┐       ┌───────────────┐
│   PDF Upload  │ ───▶ │   OCR      │ ───▶  │ GPT Extraction│
└───────────────┘       └────────────┘       └───────────────┘
       │                                             ▲
       └────────────▶ Direct parsing via Azure prebuilt models 
```

---

## Project Structure

```bash
doc-intelligence-pipeline/
├── app/
│   ├── main.py         # FastAPI entrypoint
│   ├── docint.py       # Azure Document Intelligence logic
│   ├── ocr.py          # OCR via layout model
│   ├── llm.py          # GPT-based structured extraction
│   └── models.py       # Pydantic data models
│
├── tests/
│   └── test_endpoints.py   # Endpoint tests
│
├── .env                # Local environment variables
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## Setup

Clone the repo and install dependencies (using uv):

```bash
git clone https://github.com/sophiacodesai/doc-intelligence-pipeline.git
cd doc-intelligence-pipeline
uv venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

---

## Usage

Add your Azure credentials to a .env file:
```bash
AZURE_DOCINT_KEY=...
AZURE_DOCINT_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
```
Start the API:
```bash
uvicorn app.main:app --reload
Open the interactive docs at: http://localhost:8000/docs
```
You can also launch a simple Streamlit frontend via:
```bash
streamlit run streamlit_app.py
```

---

## Prebuilt vs GPT – When to Use What?

| Scenario                          | Recommended Approach        |
|----------------------------------|-----------------------------|
| Standard invoices/paystubs       | `prebuilt-invoice`, `payStub.us` |
| Mixed templates or scans         | OCR + GPT                  |
| Custom document types (e.g. contracts) | OCR + GPT              |
| Need for speed / low latency     | Prebuilt model             |
| Need for flexibility / text logic | GPT-based parsing         |
