import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

load_dotenv()

docint_endpoint = os.getenv("AZURE_DOCINT_ENDPOINT")
docint_key = os.getenv("AZURE_DOCINT_KEY")

def _client() -> DocumentIntelligenceClient:
    """
    Creates a DocumentIntelligenceClient using your Azure credentials.
    """
    if not docint_endpoint or not docint_key:
        raise RuntimeError("Please set AZURE_DOCINT_ENDPOINT and AZURE_DOCINT_KEY in your .env file.")
    return DocumentIntelligenceClient(
        endpoint=docint_endpoint,
        credential=AzureKeyCredential(docint_key)
    )


def extract_text_from_bytes(file_bytes: bytes) -> Dict[str, Any]:
    """
    Performs OCR using Azure Document Intelligence (prebuilt-layout model).
    Returns:
    {
        "content": <plain text>,
        "raw": <full AnalyzeResult as dict>
    }
    """
    client = _client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
        content_type="application/pdf",  # only PDF files are supported but can be extended
        output_content_format="text",
    )
    result = poller.result()
    return {
        "content": getattr(result, "content", None),
        "raw": result.as_dict(),
    }


if __name__ == "__main__":
    with open("sample-invoice.pdf", "rb") as f:
        result = extract_text_from_bytes(f.read())

    print("Extracted content:")
    print(result["content"])
