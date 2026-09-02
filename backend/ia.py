import os
import tempfile
import time

from google import genai


API_KEY = os.getenv("GEMINI_API_KEY")


def transcribir_archivo(archivo):
    if not API_KEY:
        raise Exception("No se encontró GEMINI_API_KEY en Render.")

    inicio = time.time()

    print("🎙️ Preparando audio...")
    print("📦 Tamaño del audio:", len(archivo), "bytes")

    # Guardar temporalmente el audio recibido
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temporal:

        temporal.write(archivo)
        ruta_audio = temporal.name

    try:
        print("🚀 Conectando con Gemini 3.5 Transcribe...")

        client = genai.Client(
            api_key=API_KEY
        )

        # Subir audio mediante Files API
        inicio_subida = time.time()

        audio_file = client.files.upload(
            file=ruta_audio
        )

        tiempo_subida = time.time() - inicio_subida

        print(
            f"📤 Audio subido en {tiempo_subida:.2f} segundos"
        )

        print("🧠 Transcribiendo con Gemini 3.5 Transcribe...")

        inicio_gemini = time.time()

        interaction = client.interactions.create(
            model="gemini-3.5-transcribe",
            input=[
                {
                    "type": "audio",
                    "uri": audio_file.uri,
                    "mime_type": audio_file.mime_type,
                }
            ],
            generation_config={
                "transcription_config": {
                    "mode": "smart",
                    "custom_vocabulary": [
                        "vid",
                        "poda",
                        "riego",
                        "fertilización",
                        "fertilizante",
                        "fungicida",
                        "insecticida",
                        "cosecha",
                        "cuartel",
                        "parra",
                        "frutal",
                        "uva",
                        "uva de mesa",
                        "mandarina",
                        "nogal",
                        "durazno",
                        "manzano",
                        "productor",
                        "agricultor",
                        "labor agrícola"
                    ]
                }
            }
        )

        tiempo_gemini = time.time() - inicio_gemini

        print(
            f"⏱️ Gemini tardó: {tiempo_gemini:.2f} segundos"
        )

        texto = interaction.output_text

        if not texto:
            raise Exception(
                "Gemini no devolvió ninguna transcripción."
            )

        tiempo_total = time.time() - inicio

        print(
            f"✅ Transcripción completada en "
            f"{tiempo_total:.2f} segundos"
        )

        print("📝 Transcripción:", texto)

        return texto.strip()

    except Exception as error:
        print("❌ Error en Gemini Transcribe:", error)
        raise Exception(
            f"Error al transcribir el audio: {error}"
        )

    finally:
        # Eliminar archivo temporal del servidor
        if os.path.exists(ruta_audio):
            os.remove(ruta_audio)