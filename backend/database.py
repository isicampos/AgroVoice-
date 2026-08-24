import os
import httpx


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise Exception("Falta SUPABASE_URL en Render.")

if not SUPABASE_KEY:
    raise Exception("Falta SUPABASE_KEY en Render.")


BASE_URL = f"{SUPABASE_URL}/rest/v1"


HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


# =========================================================
# FUNCIÓN GENERAL
# =========================================================

def request(method, tabla, **kwargs):

    url = f"{BASE_URL}/{tabla}"

    respuesta = httpx.request(
        method,
        url,
        headers=HEADERS,
        timeout=30,
        **kwargs
    )

    if respuesta.status_code >= 400:

        raise Exception(
            f"Supabase error {respuesta.status_code}: "
            f"{respuesta.text}"
        )

    if not respuesta.text:
        return []

    return respuesta.json()


# =========================================================
# PRODUCTORES
# =========================================================

def obtener_productores():

    datos = request(
        "GET",
        "productores",
        params={
            "select": "*",
            "order": "id.asc"
        }
    )

    return [
        (
            x["id"],
            x["nombre"],
            x.get("predio"),
            x.get("cultivo")
        )
        for x in datos
    ]


def guardar_productor(nombre, predio, cultivo):

    request(
        "POST",
        "productores",
        json={
            "nombre": nombre,
            "predio": predio,
            "cultivo": cultivo
        }
    )


def actualizar_productor(id, nombre, predio, cultivo):

    request(
        "PATCH",
        "productores",
        params={
            "id": f"eq.{id}"
        },
        json={
            "nombre": nombre,
            "predio": predio,
            "cultivo": cultivo
        }
    )


def eliminar_productor(id):

    request(
        "DELETE",
        "productores",
        params={
            "id": f"eq.{id}"
        }
    )


# =========================================================
# PREDIOS
# =========================================================

def obtener_predios():

    datos = request(
        "GET",
        "predios",
        params={
            "select": "*,productores(nombre)",
            "order": "id.desc"
        }
    )

    resultado = []

    for x in datos:

        productor = x.get("productores") or {}

        resultado.append(
            (
                x["id"],
                x["nombre"],
                productor.get("nombre", ""),
                x.get("superficie"),
                x.get("region"),
                x.get("comuna")
            )
        )

    return resultado


def guardar_predio(
    nombre,
    productor_id,
    superficie,
    region,
    comuna
):

    request(
        "POST",
        "predios",
        json={
            "nombre": nombre,
            "productor_id": productor_id,
            "superficie": superficie,
            "region": region,
            "comuna": comuna
        }
    )


# =========================================================
# CUARTELES
# =========================================================

def obtener_cuarteles():

    datos = request(
        "GET",
        "cuarteles",
        params={
            "select": "*,predios(nombre)",
            "order": "id.desc"
        }
    )

    resultado = []

    for x in datos:

        predio = x.get("predios") or {}

        resultado.append(
            (
                x["id"],
                x["nombre"],
                predio.get("nombre", ""),
                x.get("cultivo"),
                x.get("variedad"),
                x.get("superficie")
            )
        )

    return resultado


def guardar_cuartel(
    nombre,
    predio_id,
    cultivo,
    variedad,
    superficie
):

    request(
        "POST",
        "cuarteles",
        json={
            "nombre": nombre,
            "predio_id": predio_id,
            "cultivo": cultivo,
            "variedad": variedad,
            "superficie": superficie
        }
    )


# =========================================================
# REGISTROS
# =========================================================

def guardar_registro(
    fecha,
    productor,
    predio,
    cuartel,
    cultivo,
    labor,
    transcripcion
):

    request(
        "POST",
        "registros",
        json={
            "fecha": fecha,
            "productor": productor,
            "predio": predio,
            "cuartel": cuartel,
            "cultivo": cultivo,
            "labor": labor,
            "transcripcion": transcripcion
        }
    )


def obtener_registros_bd():

    datos = request(
        "GET",
        "registros",
        params={
            "select": "*",
            "order": "id.desc"
        }
    )

    return [
        (
            x["id"],
            x.get("fecha"),
            x.get("productor"),
            x.get("predio"),
            x.get("cuartel"),
            x.get("cultivo"),
            x.get("labor"),
            x.get("transcripcion")
        )
        for x in datos
    ]


def actualizar_registro(
    id_registro,
    fecha,
    productor,
    predio,
    cuartel,
    cultivo,
    labor,
    transcripcion
):

    request(
        "PATCH",
        "registros",
        params={
            "id": f"eq.{id_registro}"
        },
        json={
            "fecha": fecha,
            "productor": productor,
            "predio": predio,
            "cuartel": cuartel,
            "cultivo": cultivo,
            "labor": labor,
            "transcripcion": transcripcion
        }
    )


def eliminar_registro(id_registro):

    request(
        "DELETE",
        "registros",
        params={
            "id": f"eq.{id_registro}"
        }
    )


# =========================================================
# USUARIOS
# =========================================================

def crear_usuario(
    nombre,
    correo,
    password,
    rol
):

    correo = correo.strip().lower()

    request(
        "POST",
        "usuarios",
        json={
            "nombre": nombre,
            "correo": correo,
            "password": password,
            "rol": rol
        }
    )


def obtener_usuario(correo):

    correo = correo.strip().lower()

    datos = request(
        "GET",
        "usuarios",
        params={
            "correo": f"eq.{correo}",
            "select": "*"
        }
    )

    if not datos:
        return None

    usuario = datos[0]

    return (
        usuario["id"],
        usuario["nombre"],
        usuario["correo"],
        usuario["password"],
        usuario["rol"]
    )


# =========================================================
# DASHBOARD
# =========================================================

def total_productores():

    datos = request(
        "GET",
        "productores",
        params={
            "select": "id"
        }
    )

    return len(datos)


def total_predios():

    datos = request(
        "GET",
        "predios",
        params={
            "select": "id"
        }
    )

    return len(datos)


def total_cuarteles():

    datos = request(
        "GET",
        "cuarteles",
        params={
            "select": "id"
        }
    )

    return len(datos)


def total_registros():

    datos = request(
        "GET",
        "registros",
        params={
            "select": "id"
        }
    )

    return len(datos)


def ultimos_registros():

    datos = request(
        "GET",
        "registros",
        params={
            "select": "fecha,labor,transcripcion",
            "order": "id.desc",
            "limit": "5"
        }
    )

    return [
        (
            x.get("fecha"),
            x.get("labor"),
            x.get("transcripcion")
        )
        for x in datos
    ]