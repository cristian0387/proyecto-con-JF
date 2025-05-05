from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    nombre: str
    apellido: str
    correo:str
    numtelefono: str
    password: str
    estado: Optional[int] = 1