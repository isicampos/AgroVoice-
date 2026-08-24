import os
import base64
import httpx


API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.6-flash:generateContent"
)


def transcribir_archivo(archivo):

    if not API_KEY:
        raise Exception("No se encontró GEMINI_API_KEY en Render.")

    audio_base64 = base64.b64encode(archivo).decode("utf-8")

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

    respuesta = httpx.post(
        GEMINI_URL,
        params={"key": API_KEY},
        json=datos,
        timeout=120
    )

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

    return texto.strip()