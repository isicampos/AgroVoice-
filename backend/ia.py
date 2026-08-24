import os
import base64
import httpx


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def transcribir_archivo(archivo):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("No se encontró GEMINI_API_KEY en Render.")

    audio_base64 = base64.b64encode(archivo).decode("utf-8")

    datos = {
        "contents": [
            {
                "role": "user",
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
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        },
        json=datos,
        timeout=120
    )

    if respuesta.status_code != 200:
        print("ERROR GEMINI:", respuesta.status_code)
        print("RESPUESTA GEMINI:", respuesta.text)
        raise Exception(
            f"Gemini respondió {respuesta.status_code}: {respuesta.text}"
        )

    resultado = respuesta.json()

    texto = (
        resultado["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
    )

    return texto.strip()