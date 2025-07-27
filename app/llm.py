from openai import AzureOpenAI
import os

openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

oai_client = AzureOpenAI(
    api_version="2024-06-01",
    api_key=openai_api_key,
    azure_endpoint=openai_endpoint,
)

def correct_text_with_llm(original_text: str) -> str:
    response = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Hier ist ein Text, der aus Handschrift erkannt wurde: '{original_text}'. "
                    "Korrigiere Rechtschreib- und Kontextfehler und gib den Text ohne eigene Antwort so wieder, wie er wahrscheinlich gemeint ist."
                ),
            }
        ],
        temperature=0,
    )
    return response.choices[0].message.content
