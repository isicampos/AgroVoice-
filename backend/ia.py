import os
import base64
import httpx
import time


API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.6-flash:generateContent"
)


def transcribir_archivo(archivo):

    if not API_KEY:
        raise Exception("No se encontró GEMINI_API_KEY en Render.")

    inicio = time.time()

    # -----------------------------------------
    # PREPARAR AUDIO
    # -----------------------------------------

    audio_base64 = base64.b64encode(archivo).decode("utf-8")

    print("🎙️ Preparando audio...")
    print("📦 Tamaño del audio:", len(archivo), "bytes")

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

    # -----------------------------------------
    # INTENTAR TRANSCRIPCIÓN
    # -----------------------------------------

    max_intentos = 3

    for intento in range(1, max_intentos + 1):

        print(
            f"🚀 Enviando audio a Gemini "
            f"(intento {intento}/{max_intentos})..."
        )

        inicio_gemini = time.time()

        try:

            respuesta = httpx.post(
                GEMINI_URL,
                params={"key": API_KEY},
                json=datos,
                timeout=120
            )

        except Exception as error:

            print("❌ Error de conexión con Gemini:", error)

            if intento < max_intentos:
                espera = 2 ** intento
                print(f"⏳ Reintentando en {espera} segundos...")
                time.sleep(espera)
                continue

            raise Exception(
                f"No se pudo conectar con Gemini: {error}"
            )

        tiempo_gemini = time.time() - inicio_gemini

        print(
            f"⏱️ Gemini respondió en "
            f"{tiempo_gemini:.2f} segundos"
        )

        # -----------------------------------------
        # RESPUESTA CORRECTA
        # -----------------------------------------

        if respuesta.status_code == 200:

            resultado = respuesta.json()

            try:

                texto = (
                    resultado["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )

            except (KeyError, IndexError):

                raise Exception(
                    f"Respuesta inesperada de Gemini: "
                    f"{resultado}"
                )

            tiempo_total = time.time() - inicio

            print(
                f"✅ Transcripción completada en "
                f"{tiempo_total:.2f} segundos"
            )

            return texto.strip()

        # -----------------------------------------
        # GEMINI NO DISPONIBLE TEMPORALMENTE
        # -----------------------------------------

        if respuesta.status_code in (429, 500, 502, 503, 504):

            print(
                f"⚠️ Gemini respondió "
                f"{respuesta.status_code}"
            )

            if intento < max_intentos:

                espera = 2 ** intento

                print(
                    f"⏳ Gemini está temporalmente ocupado. "
                    f"Reintentando en {espera} segundos..."
                )

                time.sleep(espera)
                continue

        # -----------------------------------------
        # OTRO ERROR
        # -----------------------------------------

        raise Exception(
            f"Gemini respondió "
            f"{respuesta.status_code}: "
            f"{respuesta.text}"
        )

    raise Exception(
        "No fue posible obtener la transcripción "
        "después de varios intentos."
    )