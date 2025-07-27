from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import io
import os

ocr_api_key = os.getenv("AZURE_OCR_API_KEY")
ocr_endpoint = os.getenv("AZURE_OCR_ENDPOINT")

def _initialize_client():
    if ocr_api_key and ocr_endpoint:
        return ComputerVisionClient(ocr_endpoint, CognitiveServicesCredentials(ocr_api_key))
    else:
        raise RuntimeError("Azure OCR credentials not set in environment variables.")

def extract_text_from_image(image_bytes: bytes) -> str:
    client = _initialize_client()
    image_stream = io.BytesIO(image_bytes)
    result = client.read_in_stream(image_stream, language="de", raw=True)
    operation_id = result.headers["Operation-Location"].split("/")[-1]

    while True:
        status = client.get_read_result(operation_id)
        if status.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    result = client.get_read_result(operation_id)
    if result.status == OperationStatusCodes.succeeded:
        lines = [line.text for line in result.analyze_result.read_results[0].lines]
        return "\n".join(lines)
    return ""
