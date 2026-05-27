from pydantic import BaseModel

# Para CREAR una opinión
class OpinionCreate(BaseModel):
    cafeteria: str
    opinion: str
    sentimiento: str

# Para DEVOLVER una opinión
class OpinionOut(BaseModel):
    id: str
    cafeteria: str
    opinion: str
    sentimiento: str