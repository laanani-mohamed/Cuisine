from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Cuisine, Placard, CoutAnalyse
from utils import calculer_cout_total, get_cout_par_placard, get_repartition_accessoires
import db

app = FastAPI(
    title="Kitchen Management API",
    description="API pour gérer les cuisines, placards et accessoires",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Kitchen Management",
        "documentation": "/docs"
    }

@app.get("/cuisines")
def get_cuisines():
    """Récupère la liste de toutes les cuisines"""
    cuisines = db.get_all_cuisines()
    return {"cuisines": cuisines}

@app.get("/cuisines/{id_cuisine}")
def get_cuisine(id_cuisine: int):
    """Récupère les détails d'une cuisine"""
    cuisine = db.get_cuisine_by_id(id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")
    return cuisine

@app.get("/placards/{id_cuisine}")
def get_placards(id_cuisine: int):
    """Récupère tous les placards d'une cuisine"""
    # Vérifier que la cuisine existe
    cuisine = db.get_cuisine_by_id(id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")

    placards = db.get_placards_by_cuisine(id_cuisine)
    return {"id_cuisine": id_cuisine, "placards": placards}

@app.post("/placard")
def create_placard(placard: Placard):
    """Ajoute un nouveau placard"""
    # Vérifier que la cuisine existe
    cuisine = db.get_cuisine_by_id(placard.id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")

    placard_id = db.add_placard(
        placard.id_cuisine,
        placard.type,
        placard.largeur,
        placard.hauteur,
        placard.profondeur,
        placard.couleur
    )

    return {
        "message": "Placard ajouté avec succès",
        "id": placard_id
    }

@app.post("/cuisine")
def create_cuisine(cuisine: Cuisine):
    """Ajoute une nouvelle cuisine"""
    cuisine_id = db.add_cuisine(
        cuisine.nom,
        cuisine.superficie,
        cuisine.emplacement
    )

    return {
        "message": "Cuisine ajoutée avec succès",
        "id": cuisine_id
    }

@app.get("/analyse/cout/{id_cuisine}")
def analyse_cout(id_cuisine: int):
    """Calcule le coût total d'une cuisine"""
    # Vérifier que la cuisine existe
    cuisine = db.get_cuisine_by_id(id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")

    total = calculer_cout_total(id_cuisine)
    return {
        "id_cuisine": id_cuisine,
        "cout_total": round(total, 2)
    }

@app.get("/analyse/cout-par-placard/{id_cuisine}")
def analyse_cout_par_placard(id_cuisine: int):
    """Retourne le coût par placard pour une cuisine"""
    # Vérifier que la cuisine existe
    cuisine = db.get_cuisine_by_id(id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")

    placards = get_cout_par_placard(id_cuisine)
    return {
        "id_cuisine": id_cuisine,
        "placards": placards
    }

@app.get("/analyse/repartition-accessoires/{id_cuisine}")
def analyse_repartition(id_cuisine: int):
    """Retourne la répartition des accessoires par catégorie"""
    # Vérifier que la cuisine existe
    cuisine = db.get_cuisine_by_id(id_cuisine)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine non trouvée")

    repartition = get_repartition_accessoires(id_cuisine)
    return {
        "id_cuisine": id_cuisine,
        "repartition": repartition
    }

@app.get("/accessoires")
def get_accessoires():
    """Récupère la liste de tous les accessoires"""
    accessoires = db.get_all_accessoires()
    return {"accessoires": accessoires}
