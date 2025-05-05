from typing import Union
from pydantic import BaseModel
from models.user_model import User

class Folio(BaseModel):
    nombre: str
    apellido: str
    numcaso: int
    numtelefono: int
    usuario: Union[int, User]