from pydantic import BaseModel
from typing import Optional

class Cuisine(BaseModel):
    id: Optional[int] = None
    nom: str
    superficie: float
    emplacement: str

class Placard(BaseModel):
    id: Optional[int] = None
    id_cuisine: int
    type: str
    largeur: float
    hauteur: float
    profondeur: float
    couleur: str

class Accessoire(BaseModel):
    id: Optional[int] = None
    nom: str
    categorie: str
    prix_unitaire: float

class CoutAnalyse(BaseModel):
    id_cuisine: int
    cout_total: float
