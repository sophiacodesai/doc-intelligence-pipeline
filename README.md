🧾 Doc Intelligence Pipeline (FastAPI)

This project showcases two flexible approaches for document information extraction using Azure services and LLMs – ideal for real-world OCR, invoice parsing, or paystub extraction use cases.

It highlights the trade-offs between specialized prebuilt models and a generalized OCR + LLM pipeline.

✨ Features

FastAPI backend with three POST endpoints:

/extract/invoice → Structured extraction via Azure Document Intelligence prebuilt-invoice

/extract/paystub → Optional paystub extraction via prebuilt-payStub.us

/extract/ocr-llm → Generalized pipeline: OCR layout + GPT-4o postprocessing

Modular architecture:

docint.py → Azure Document Intelligence extraction

ocr.py → Layout-based OCR using Azure DI prebuilt-layout

llm.py → GPT-based correction or structured field extraction

models.py → Pydantic schemas (optional for input/output)

Environment-based configuration using .env

⚙️ Use Cases

Automated invoice or pay stub field extraction

OCR + GPT-4o pipeline for arbitrary documents with fuzzy layout

Playground for structured LLM output, e.g. JSON schema extraction

📦 Installation
Requirements

Python 3.10+

Azure resources:

✅ Document Intelligence
 (endpoint + key)

✅ Azure OpenAI
 (endpoint + key)

Setup
# Clone the repo
git clone https://github.com/your-username/doc-intelligence-pipeline.git
cd doc-intelligence-pipeline

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -U pip
pip install -r requirements.txt

.env Example
# .env
AZURE_DOCINT_KEY=your_document_intelligence_key
AZURE_DOCINT_ENDPOINT=https://your-resource.cognitiveservices.azure.com/

AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/

🚀 Run Locally
uvicorn app.main:app --reload


Access the interactive Swagger UI at http://localhost:8000/docs

🧠 Models Used
Component	Model	Purpose
Azure DI	prebuilt-invoice	Invoice field extraction
Azure DI	prebuilt-payStub.us	(Optional) Paystub fields
Azure DI	prebuilt-layout	General-purpose OCR
Azure OpenAI	gpt-4o	Correction & JSON extraction
🛠 Example Extensions

Fine-tune your own DI custom model

Integrate a document database (e.g. Cosmos DB, Supabase)

Add file upload via Streamlit or React frontend

Use LangChain or Guardrails for LLM output validation

💡 Why This Matters

This project demonstrates your ability to:

Work with enterprise-grade Azure APIs (OCR, OpenAI)

Build clean, production-style Python APIs with FastAPI

Handle real-world documents, not just idealized samples

Use GPT models for practical, structured output (not just chat)

Perfect for showcasing your skills in:

AI Engineering

Document Automation

GPT-based Information Extraction

Modern API Development

