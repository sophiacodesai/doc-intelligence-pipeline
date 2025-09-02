from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
import traceback

from app.docint import analyze_invoice_from_bytes
# Optional: Pay Stub (falls du die Funktion gebaut hast)
from app.docint import analyze_paystub_from_bytes  # kannst du löschen, falls nicht genutzt

# OCR+LLM
from app.ocr import extract_text_from_bytes
from app.llm import structured_extract

app = FastAPI(title="Doc Intelligence Pipeline")

PDF_ONLY_MSG = "Only PDF files are supported."

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract/invoice")
async def extract_invoice(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=PDF_ONLY_MSG)

    data = await file.read()
    try:
        result = analyze_invoice_from_bytes(data)
        # du gibst fürs UI nur das „extracted“ zurück; bei Debugbedarf kannst du auch result["raw"] mitsenden
        return JSONResponse(content=result["extracted"])
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{e}\n{tb}")

# Optional – falls du Pay-Stub im Portfolio zeigen willst:
@app.post("/extract/paystub")
async def extract_paystub(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=PDF_ONLY_MSG)

    data = await file.read()
    try:
        result = analyze_paystub_from_bytes(data)
        return JSONResponse(content=result["extracted"])
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{e}\n{tb}")

# OCR -> LLM: generischer Weg, um die Gegenüberstellung zu zeigen
@app.post("/extract/ocr-llm")
async def extract_ocr_llm(
    file: UploadFile = File(...),
    task: str = Query(
        default="Extract invoice fields (id, date, vendor, total, items)",
        description="Freitext-Aufgabe für die LLM-Extraktion."
    ),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=PDF_ONLY_MSG)

    data = await file.read()
    try:
        ocr = extract_text_from_bytes(data, markdown=False, high_res=True)
        text = ocr.get("content") or ""
        llm = structured_extract(text, task=task, schema_hint=None)
        # Für Transparenz kannst du die Anzahl Zeichen ausgeben
        return JSONResponse(content={
            "ocr": {"length": len(text)},
            "extracted": llm
        })
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{e}\n{tb}")
