import tempfile
import os
import whisper

modelo = None


def obtener_modelo():

    global modelo

    if modelo is None:
        modelo = whisper.load_model("base")

    return modelo


def transcribir_archivo(archivo):

    modelo = obtener_modelo()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temporal:

        temporal.write(archivo)
        ruta = temporal.name

    try:

        resultado = modelo.transcribe(
            ruta,
            language="es"
        )

        return resultado.get(
            "text",
            ""
        ).strip()

    finally:

        if os.path.exists(ruta):
            os.remove(ruta)