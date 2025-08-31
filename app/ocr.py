# app/ocr.py
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

load_dotenv()
ENDPOINT = os.getenv("AZURE_DOCINT_ENDPOINT")
KEY = os.getenv("AZURE_DOCINT_KEY")

def _client() -> DocumentIntelligenceClient:
    if not ENDPOINT or not KEY:
        raise RuntimeError("Bitte AZURE_DOCINT_ENDPOINT und AZURE_DOCINT_KEY in .env setzen.")
    return DocumentIntelligenceClient(ENDPOINT, AzureKeyCredential(KEY))

def extract_text_from_bytes(
    file_bytes: bytes,
    *,
    markdown: bool = False,
    high_res: bool = True,
) -> Dict[str, Any]:
    """
    OCR via Document Intelligence (prebuilt-layout).
    Gibt {"content": <text|markdown>, "raw": <AnalyzeResult as dict>} zurück.
    """
    client = _client()
    features: List[str] = ["ocrHighResolution"] if high_res else []
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=file_bytes,
        content_type="application/pdf",
        features=features,
        output_content_format=("markdown" if markdown else "text"),
    )
    result = poller.result()
    return {
        "content": getattr(result, "content", None),
        "raw": result.as_dict(),
    }
