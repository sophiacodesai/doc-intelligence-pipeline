import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

load_dotenv()
ENDPOINT = os.getenv("AZURE_DOCINT_ENDPOINT")
KEY = os.getenv("AZURE_DOCINT_KEY")

MODEL_INVOICE = "prebuilt-invoice"
MODEL_PAYSTUB = "prebuilt-payStub.us"  # für Gehaltsabrechnungen

def _client() -> DocumentIntelligenceClient:
    if not ENDPOINT or not KEY:
        raise RuntimeError("Bitte AZURE_DOCINT_ENDPOINT und AZURE_DOCINT_KEY in .env setzen.")
    return DocumentIntelligenceClient(ENDPOINT, AzureKeyCredential(KEY))

def analyze_invoice_from_bytes(file_bytes: bytes) -> Dict[str, Any]:
    """
    Strukturierte Extraktion (Invoice). Gibt {"extracted": {...}, "raw": {...}} zurück.
    """
    client = _client()
    poller = client.begin_analyze_document(
        MODEL_INVOICE,
        body=file_bytes,                      # <-- wichtig: body (Bytes)
        content_type="application/pdf",       # <-- passend zu Bytes
    )
    result = poller.result()

    docs = result.documents or []
    if not docs:
        return {"extracted": {}, "raw": result.as_dict()}

    f = docs[0].fields or {}

    def _val(name: str):
        fld = f.get(name)
        return getattr(fld, "value", None) if fld else None

    def _content(name: str):
        fld = f.get(name)
        return getattr(fld, "content", None) if fld else None

    extracted = {
        "invoiceId": _val("InvoiceId"),
        "invoiceDate": _val("InvoiceDate"),
        "dueDate": _val("DueDate"),
        "vendorName": _val("VendorName"),
        "customerName": _val("CustomerName"),
        "billingAddress": _content("BillingAddress"),
        "shippingAddress": _content("ShippingAddress"),
        "total": _val("InvoiceTotal"),
        "subTotal": _val("SubTotal"),
        "tax": _val("TotalTax"),
        "purchaseOrder": _val("PurchaseOrder"),
        "items": [],
    }

    items = f.get("Items")
    if items and getattr(items, "value", None):
        for it in items.value:
            p = getattr(it, "properties", {}) or {}
            getp = lambda k: (getattr(p.get(k), "value", None) if p.get(k) else None)
            extracted["items"].append({
                "description": getp("Description"),
                "quantity": getp("Quantity"),
                "unitPrice": getp("UnitPrice"),
                "amount": getp("Amount"),
            })

    return {"extracted": extracted, "raw": result.as_dict()}

def analyze_paystub_from_bytes(file_bytes: bytes) -> Dict[str, Any]:
    """
    Optional: Gehaltsabrechnung (Pay Stub).
    """
    client = _client()
    poller = client.begin_analyze_document(
        MODEL_PAYSTUB,
        body=file_bytes,
        content_type="application/pdf",
    )
    result = poller.result()
    docs = result.documents or []
    f = (docs[0].fields or {}) if docs else {}

    def _val(name: str):
        fld = f.get(name)
        return getattr(fld, "value", None) if fld else None

    extracted = {
        "employerName": _val("EmployerName"),
        "employeeName": _val("EmployeeName"),
        "periodStart": _val("PayPeriodStartDate"),
        "periodEnd": _val("PayPeriodEndDate"),
        "grossPay": _val("GrossPayYtd") or _val("GrossPay"),
        "netPay": _val("NetPayYtd") or _val("NetPay"),
        "taxes": {
            "federal": _val("FederalTax"),
            "state": _val("StateTax"),
            "medicare": _val("MedicareTax"),
            "socialSecurity": _val("SocialSecurityTax"),
        },
    }
    return {"extracted": extracted, "raw": result.as_dict()}
