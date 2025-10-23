import sqlite3

DATABASE_PATH = "data/kitchen.db"

def calculer_cout_total(id_cuisine: int) -> float:
    """
    Calcule le coût total d'une cuisine en additionnant
    les prix de tous les accessoires utilisés dans ses placards
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(a.prix_unitaire * pa.quantite) as total
        FROM Accessoire a
        JOIN Placard_Accessoire pa ON a.id = pa.id_accessoire
        JOIN Placard p ON p.id = pa.id_placard
        WHERE p.id_cuisine = ?
    """, (id_cuisine,))

    result = cur.fetchone()[0]
    conn.close()

    return result if result else 0.0

def get_cout_par_placard(id_cuisine: int):
    """
    Retourne le coût par placard pour une cuisine donnée
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.type,
            p.couleur,
            SUM(a.prix_unitaire * pa.quantite) as cout_total
        FROM Placard p
        LEFT JOIN Placard_Accessoire pa ON p.id = pa.id_placard
        LEFT JOIN Accessoire a ON a.id = pa.id_accessoire
        WHERE p.id_cuisine = ?
        GROUP BY p.id, p.type, p.couleur
    """, (id_cuisine,))

    placards = [dict(row) for row in cur.fetchall()]
    conn.close()

    return placards

def get_repartition_accessoires(id_cuisine: int):
    """
    Retourne la répartition des accessoires par catégorie pour une cuisine
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.categorie,
            SUM(pa.quantite) as quantite_totale,
            SUM(a.prix_unitaire * pa.quantite) as cout_total
        FROM Accessoire a
        JOIN Placard_Accessoire pa ON a.id = pa.id_accessoire
        JOIN Placard p ON p.id = pa.id_placard
        WHERE p.id_cuisine = ?
        GROUP BY a.categorie
    """, (id_cuisine,))

    repartition = [dict(row) for row in cur.fetchall()]
    conn.close()

    return repartition
