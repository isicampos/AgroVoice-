from datetime import date
from pydantic import BaseModel


# =====================================
# PRODUCTORES
# =====================================

class Productor(BaseModel):
    id: int
    nombre: str
    predio: str
    cultivo: str


class NuevoProductor(BaseModel):
    nombre: str
    predio: str
    cultivo: str


# =====================================
# REGISTROS
# =====================================

class Registro(BaseModel):
    id: int
    fecha: str
    productor: str
    predio: str
    cuartel: str
    cultivo: str
    labor: str
    transcripcion: str


class NuevoRegistro(BaseModel):
    fecha: str
    productor: str
    predio: str
    cuartel: str
    cultivo: str
    labor: str
    transcripcion: str
# =====================================
# USUARIOS
# =====================================

class Usuario(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str


class NuevoUsuario(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: str


class Login(BaseModel):
    correo: str
    password: str
class Usuario(BaseModel):

    id:int

    nombre:str

    correo:str

    rol:str


class Login(BaseModel):

    correo:str

    password:str

class Predio(BaseModel):
    id: int
    nombre: str
    productor: str
    superficie: float
    region: str
    comuna: str


class NuevoPredio(BaseModel):
    nombre: str
    productor_id: int
    superficie: float
    region: str
    comuna: str

class Cuartel(BaseModel):
    id: int
    nombre: str
    predio: str
    cultivo: str
    variedad: str
    superficie: float


class NuevoCuartel(BaseModel):
    nombre: str
    predio_id: int
    cultivo: str
    variedad: str
    superficie: float

class RegistroCompleto(BaseModel):
    id:int
    fecha:str
    productor:str
    predio:str
    cuartel:str
    cultivo:str
    labor:str
    descripcion:str


class NuevoRegistroCompleto(BaseModel):
    fecha:str
    productor_id:int
    predio_id:int
    cuartel_id:int
    cultivo:str
    labor:str
    descripcion:str