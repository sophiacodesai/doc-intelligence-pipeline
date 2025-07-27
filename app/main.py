from fastapi import FastAPI, File, UploadFile, HTTPException
from app.ocr import extract_text_from_image
from app.llm import correct_text_with_llm

app = FastAPI()

@app.post("/recognize-handwriting")
async def recognize_handwriting(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        raw_text = extract_text_from_image(image_bytes)
        if not raw_text:
            return {"message": "Kein Text erkannt"}

        corrected_text = correct_text_with_llm(raw_text)
        return {"text": corrected_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
