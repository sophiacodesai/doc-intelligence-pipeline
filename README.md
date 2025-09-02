# Document Intelligence Pipeline

This repository demonstrates two distinct approaches for extracting structured information from documents:

1. **Structured extraction using Azure Document Intelligence (e.g., invoices)**
2. **OCR-based text extraction with downstream LLM processing (GPT)**

---

## Features

- Invoice parsing using Azure's prebuilt model (`prebuilt-invoice`)
- Pay stub extraction (optional, `prebuilt-payStub.us`)
- OCR extraction from scanned or unstructured documents
- LLM-based parsing and structuring via Azure OpenAI

---

## API Overview

This FastAPI-based backend provides the following REST endpoints:

| Endpoint                 | Description                                     |
|--------------------------|-------------------------------------------------|
| `GET /health`            | Health check                                   |
| `POST /extract/invoice`  | Extract structured invoice data                |
| `POST /extract/paystub`  | Extract data from US pay stubs (optional)      |
| `POST /extract/ocr-llm`  | Extract via OCR + GPT (free-text instructions) |

---

## Example Architecture

```text
┌───────────────┐       ┌────────────┐       ┌───────────────┐
│   PDF Upload  │ ───▶ │   OCR      │ ───▶  │ GPT Extraction│
└───────────────┘       └────────────┘       └───────────────┘
       │                                       ▲
       └────────────▶ Direct parsing via Document Intelligence (optional)
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
uv venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

---

## Usage

Add your Azure credentials to a .env file:

AZURE_DOCINT_KEY=...
AZURE_DOCINT_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...

Start the API:
uvicorn app.main:app --reload
Open the interactive docs at: http://localhost:8000/docs

---

## Why This Project?

This repository showcases how to bridge traditional document models with GPT-based flexibility, ideal for:

- Automating invoice or payslip parsing
- Handling OCR-based document flows
- Comparing rule-based vs. generative approaches
