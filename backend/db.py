import sqlite3
from typing import Optional

DATABASE_PATH = "data/kitchen.db"

def get_connection():
    """Retourne une connexion à la base de données"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

def get_all_cuisines():
    """Récupère toutes les cuisines"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cuisine")
    cuisines = [dict(row) for row in cur.fetchall()]
    conn.close()
    return cuisines

def get_cuisine_by_id(id_cuisine: int):
    """Récupère une cuisine par son ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cuisine WHERE id = ?", (id_cuisine,))
    cuisine = cur.fetchone()
    conn.close()
    return dict(cuisine) if cuisine else None

def get_placards_by_cuisine(id_cuisine: int):
    """Récupère tous les placards d'une cuisine"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Placard WHERE id_cuisine = ?", (id_cuisine,))
    placards = [dict(row) for row in cur.fetchall()]
    conn.close()
    return placards

def add_placard(id_cuisine: int, type: str, largeur: float, hauteur: float,
                profondeur: float, couleur: str):
    """Ajoute un nouveau placard"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_cuisine, type, largeur, hauteur, profondeur, couleur))
    placard_id = cur.lastrowid
    conn.commit()
    conn.close()
    return placard_id

def add_cuisine(nom: str, superficie: float, emplacement: str):
    """Ajoute une nouvelle cuisine"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Cuisine (nom, superficie, emplacement)
        VALUES (?, ?, ?)
    """, (nom, superficie, emplacement))
    cuisine_id = cur.lastrowid
    conn.commit()
    conn.close()
    return cuisine_id

def get_all_accessoires():
    """Récupère tous les accessoires"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Accessoire")
    accessoires = [dict(row) for row in cur.fetchall()]
    conn.close()
    return accessoires
