import streamlit as st
import requests
from PIL import Image
import time

st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 2])
with col1:
    st.image("tensora_logo.png", width=200)  # Optional
with col2:
    st.title("Document Intelligence – Demo UI")
    st.markdown("Vergleich: Prebuilt-Modell vs. OCR → LLM")

st.markdown("## 📄 PDF hochladen")
uploaded_file = st.file_uploader("Lade eine PDF-Datei hoch", type=["pdf"])

# Auswahl des Extraktionsmodus
mode = st.radio(
    "Extraktionsweg auswählen:",
    ["Prebuilt-Invoice (Azure)", "OCR → LLM"],
    horizontal=True
)

# POST-Anfrage an FastAPI-Backend
def request_prebuilt_invoice(file):
    url = "http://127.0.0.1:8000/extract/invoice"
    return requests.post(url, files={"file": file})

def request_ocr_llm(file):
    url = "http://127.0.0.1:8000/extract/ocr-llm"
    return requests.post(url, files={"file": file})


if st.button("Extrahieren"):
    if uploaded_file:
        with st.spinner("Verarbeite Dokument..."):
            time.sleep(1)

            try:
                if mode == "Prebuilt-Invoice (Azure)":
                    response = request_prebuilt_invoice(uploaded_file)
                else:
                    response = request_ocr_llm(uploaded_file)

                response.raise_for_status()
                result = response.json()
                st.success("Extraktion erfolgreich!")

                st.markdown("## 🧾 Extrahierte Daten:")
                for key, value in result.items():
                    st.text_input(key, str(value), disabled=True)

            except Exception as e:
                st.error(f"Fehler: {e}")
    else:
        st.warning("Bitte lade zuerst eine Datei hoch.")
