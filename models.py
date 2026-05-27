from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class OpinionModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    cafeteria: str
    opinion: str
    sentimiento: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True