from pydantic import BaseModel

class CorrectedTextResponse(BaseModel):
    text: str
