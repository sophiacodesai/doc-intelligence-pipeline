import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

load_dotenv()

azure_docint_endpoint = os.getenv("AZURE_DOCINT_ENDPOINT")
azure_docint_key = os.getenv("AZURE_DOCINT_KEY")

def _client() -> DocumentIntelligenceClient:
    """
    Erstellt einen DocumentIntelligenceClient mit Azure Key Credential.
    """
    if not azure_docint_endpoint or not azure_docint_key:
        raise RuntimeError("Bitte AZURE_DOCINT_ENDPOINT und AZURE_DOCINT_KEY in der .env-Datei setzen.")
    return DocumentIntelligenceClient(
        endpoint=azure_docint_endpoint,
        credential=AzureKeyCredential(azure_docint_key)
    )

def extract_text_from_bytes(
    file_bytes: bytes,
    *,
    markdown: bool = False,
    high_res: bool = True,
) -> Dict[str, Any]:
    """
    Führt OCR durch (Azure Document Intelligence – prebuilt-layout Modell).

    Gibt folgenden Dictionary zurück:
    {
        "content": <extrahierter Text oder Markdown>,
        "raw": <komplette AnalyzeResult-Struktur als Dictionary>
    }

    Parameter:
    - file_bytes: PDF-Datei als Byte-Stream
    - markdown: Gibt Markdown statt einfachem Text zurück (z. B. mit Listen/Überschriften)
    - high_res: Aktiviert ocrHighResolution-Feature (besser bei Scans, etwas langsamer)
    """
    client = _client()
    features: List[str] = ["ocrHighResolution"] if high_res else []

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
        content_type="application/pdf",  
        features=features,
        output_content_format="markdown" if markdown else "text",
    )

    result = poller.result()

    return {
        "content": getattr(result, "content", None),
        "raw": result.as_dict(),
    }