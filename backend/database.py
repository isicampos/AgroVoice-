import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "agrovoice.db")


# ==========================================
# CONEXIÓN
# ==========================================

def conectar():
    return sqlite3.connect(DB)

# ==========================================
# CREAR BASE DE DATOS
# ==========================================

def crear_bd():

    conexion = conectar()
    cursor = conexion.cursor()

    # -------------------------
    # PRODUCTORES
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS productores(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT,

        predio TEXT,

        cultivo TEXT

    )

    """)

    # -------------------------
    # REGISTROS
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS registros(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT,

        productor TEXT,

        predio TEXT,

        cuartel TEXT,

        cultivo TEXT,

        labor TEXT,

        transcripcion TEXT

    )

    """)

    # -------------------------
    # USUARIOS
    # -------------------------

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT,

        correo TEXT UNIQUE,

        password TEXT,

        rol TEXT

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS predios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT,

        productor_id INTEGER,

        superficie REAL,

        region TEXT,

        comuna TEXT,

        FOREIGN KEY(productor_id) REFERENCES productores(id)

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS cuarteles(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT,

        predio_id INTEGER,

        cultivo TEXT,

        variedad TEXT,

        superficie REAL,

        FOREIGN KEY(predio_id) REFERENCES predios(id)

    )

    """)

    conexion.commit()
    conexion.close()


# ==========================================
# PRODUCTORES
# ==========================================

def obtener_productores():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    SELECT
        id,
        nombre,
        predio,
        cultivo

    FROM productores

    ORDER BY id

    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

# ==========================================
# REGISTROS
# ==========================================

def guardar_registro(

    fecha,

    productor,

    predio,

    cuartel,

    cultivo,

    labor,

    transcripcion

):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    INSERT INTO registros(

        fecha,

        productor,

        predio,

        cuartel,

        cultivo,

        labor,

        transcripcion

    )

    VALUES(?,?,?,?,?,?,?)

    """,(

        fecha,

        productor,

        predio,

        cuartel,

        cultivo,

        labor,

        transcripcion

    ))

    conexion.commit()

    conexion.close()


def obtener_registros_bd():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    SELECT

        id,

        fecha,

        productor,

        predio,

        cuartel,

        cultivo,

        labor,

        transcripcion

    FROM registros

    ORDER BY id DESC

    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos

# ==========================================
# ELIMINAR REGISTRO
# ==========================================

def eliminar_registro(id_registro):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    DELETE FROM registros

    WHERE id=?

    """,(id_registro,))

    conexion.commit()

    conexion.close()

    # ==========================================
# ACTUALIZAR REGISTRO
# ==========================================

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

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    UPDATE registros

    SET

        fecha=?,

        productor=?,

        predio=?,

        cuartel=?,

        cultivo=?,

        labor=?,

        transcripcion=?

    WHERE id=?

    """,(

        fecha,

        productor,

        predio,

        cuartel,

        cultivo,

        labor,

        transcripcion,

        id_registro

    ))

    conexion.commit()

    conexion.close()


def guardar_productor(
    nombre,
    predio,
    cultivo
):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    INSERT INTO productores(

        nombre,

        predio,

        cultivo

    )

    VALUES(?,?,?)

    """,(

        nombre,

        predio,

        cultivo

    ))

    conexion.commit()

    conexion.close()


# ==========================================
# USUARIOS
# ==========================================

def crear_usuario(
    nombre,
    correo,
    password,
    rol
):

    correo = correo.strip().lower()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO usuarios(
            nombre,
            correo,
            password,
            rol
        )
        VALUES(?,?,?,?)
    """,(
        nombre,
        correo,
        password,
        rol
    ))

    conexion.commit()
    conexion.close()

def obtener_usuario(correo):

    correo = correo.strip().lower()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            correo,
            password,
            rol
        FROM usuarios
        WHERE correo=?
    """,(correo,))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario

def eliminar_productor(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productores WHERE id=?", (id,))

    conexion.commit()

    conexion.close()


def actualizar_productor(id, nombre, predio, cultivo):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    UPDATE productores

    SET

        nombre=?,

        predio=?,

        cultivo=?

    WHERE id=?

    """,(

        nombre,

        predio,

        cultivo,

        id

    ))

    conexion.commit()

    conexion.close()


def guardar_predio(nombre, productor_id, superficie, region, comuna):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""

    INSERT INTO predios(

        nombre,

        productor_id,

        superficie,

        region,

        comuna

    )

    VALUES(?,?,?,?,?)

    """,(

        nombre,

        productor_id,

        superficie,

        region,

        comuna

    ))

    conexion.commit()

    conexion.close()


def obtener_predios():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""

    SELECT

        predios.id,

        predios.nombre,

        productores.nombre,

        predios.superficie,

        predios.region,

        predios.comuna

    FROM predios

    INNER JOIN productores

    ON predios.productor_id=productores.id

    ORDER BY predios.id DESC

    """)

    datos=cursor.fetchall()

    conexion.close()

    return datos

def guardar_cuartel(nombre,predio_id,cultivo,variedad,superficie):

    conexion=conectar()

    cursor=conexion.cursor()

    cursor.execute("""

    INSERT INTO cuarteles(

        nombre,

        predio_id,

        cultivo,

        variedad,

        superficie

    )

    VALUES(?,?,?,?,?)

    """,(

        nombre,

        predio_id,

        cultivo,

        variedad,

        superficie

    ))

    conexion.commit()

    conexion.close()


def obtener_cuarteles():

    conexion=conectar()

    cursor=conexion.cursor()

    cursor.execute("""

    SELECT

        cuarteles.id,

        cuarteles.nombre,

        predios.nombre,

        cuarteles.cultivo,

        cuarteles.variedad,

        cuarteles.superficie

    FROM cuarteles

    INNER JOIN predios

    ON predios.id=cuarteles.predio_id

    ORDER BY cuarteles.id DESC

    """)

    datos=cursor.fetchall()

    conexion.close()

    return datos
def guardar_registro(
    fecha,
    productor_id,
    predio_id,
    cuartel_id,
    cultivo,
    labor,
    descripcion
):

    conexion=conectar()
    cursor=conexion.cursor()

    cursor.execute("""

    INSERT INTO registros(

        fecha,
        productor_id,
        predio_id,
        cuartel_id,
        cultivo,
        labor,
        descripcion

    )

    VALUES(?,?,?,?,?,?,?)

    """,(

        fecha,
        productor_id,
        predio_id,
        cuartel_id,
        cultivo,
        labor,
        descripcion

    ))

    conexion.commit()
    conexion.close()

def total_productores():
    conexion=conectar()
    cursor=conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM productores")

    total=cursor.fetchone()[0]

    conexion.close()

    return total


def total_predios():

    conexion=conectar()
    cursor=conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM predios")

    total=cursor.fetchone()[0]

    conexion.close()

    return total


def total_cuarteles():

    conexion=conectar()
    cursor=conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM cuarteles")

    total=cursor.fetchone()[0]

    conexion.close()

    return total


def total_registros():

    conexion=conectar()
    cursor=conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM registros")

    total=cursor.fetchone()[0]

    conexion.close()

    return total
def ultimos_registros():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""

    SELECT

        fecha,

        labor,

        descripcion

    FROM registros

    ORDER BY id DESC

    LIMIT 5

    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos