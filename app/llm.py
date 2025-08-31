import os
from openai import AzureOpenAI

openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not openai_api_key or not openai_endpoint:
    raise RuntimeError("Bitte AZURE_OPENAI_API_KEY und AZURE_OPENAI_ENDPOINT in .env setzen.")

oai_client = AzureOpenAI(
    api_version="2024-06-01",
    api_key=openai_api_key,
    azure_endpoint=openai_endpoint,
)

def correct_text_with_llm(original_text: str) -> str:
    resp = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": (
                "Hier ist ein Text, der aus Handschrift erkannt wurde:\n"
                f"{original_text}\n\n"
                "Korrigiere Rechtschreib- und Kontextfehler und gib nur den bereinigten Text zurück."
            ),
        }],
        temperature=0,
    )
    return resp.choices[0].message.content

def structured_extract(text: str, task: str, schema_hint: dict | None = None) -> dict:
    """
    Generischer Extraktor: definiere in 'task', was du haben willst,
    z. B. 'Extract invoice fields (id, date, vendor, total, items ...)'.
    """
    sys = (
        "You are a precise information extraction assistant. "
        "Return strictly valid JSON matching the user's request. "
        "If a field is missing, set it to null. Do not add extra commentary."
    )
    user = f"Task: {task}\n\nText:\n{text}\n\n"
    if schema_hint:
        user += f"Output MUST match this JSON schema (keys/types): {schema_hint}"

    resp = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": sys},
                  {"role": "user", "content": user}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    import json
    return json.loads(resp.choices[0].message.content)
