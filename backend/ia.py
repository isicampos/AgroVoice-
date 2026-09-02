import os
import base64
import httpx
import time


API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

def transcribir_archivo(archivo):

    if not API_KEY:
        raise Exception("No se encontró GEMINI_API_KEY en Render.")

    inicio = time.time()

    audio_base64 = base64.b64encode(archivo).decode("utf-8")

    print("🎙️ Preparando audio...")
    print("📦 Tamaño original:", len(archivo), "bytes")

    datos = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Transcribe exactamente este audio en español. "
                            "Devuelve solamente la transcripción, "
                            "sin explicaciones ni comentarios."
                        )
                    },
                    {
                        "inline_data": {
                            "mime_type": "audio/wav",
                            "data": audio_base64
                        }
                    }
                ]
            }
        ]
    }

    print("🚀 Enviando audio a Gemini...")

    inicio_gemini = time.time()

    respuesta = httpx.post(
        GEMINI_URL,
        params={"key": API_KEY},
        json=datos,
        timeout=120
    )

    tiempo_gemini = time.time() - inicio_gemini

    print(f"⏱️ Gemini tardó: {tiempo_gemini:.2f} segundos")

    if respuesta.status_code != 200:
        raise Exception(
            f"Gemini respondió {respuesta.status_code}: "
            f"{respuesta.text}"
        )

    resultado = respuesta.json()

    texto = (
        resultado["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
    )

    tiempo_total = time.time() - inicio

    print(f"✅ Tiempo total de transcripción: {tiempo_total:.2f} segundos")

    return texto.strip()