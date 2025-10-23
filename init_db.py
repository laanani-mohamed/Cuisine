import sqlite3
import os

def init_database():
    """Initialise la base de données avec les tables nécessaires"""

    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)

    # Connexion à la base de données
    conn = sqlite3.connect("data/kitchen.db")
    cur = conn.cursor()

    # Création de la table Cuisine
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Cuisine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            superficie REAL,
            emplacement TEXT
        )
    """)

    # Création de la table Placard
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Placard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuisine INTEGER NOT NULL,
            type TEXT,
            largeur REAL,
            hauteur REAL,
            profondeur REAL,
            couleur TEXT,
            FOREIGN KEY (id_cuisine) REFERENCES Cuisine(id)
        )
    """)

    # Création de la table Compartiment
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Compartiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_placard INTEGER NOT NULL,
            type TEXT,
            hauteur REAL,
            largeur REAL,
            profondeur REAL,
            FOREIGN KEY (id_placard) REFERENCES Placard(id)
        )
    """)

    # Création de la table Accessoire
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Accessoire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            categorie TEXT,
            prix_unitaire REAL NOT NULL
        )
    """)

    # Création de la table Placard_Accessoire
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Placard_Accessoire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_placard INTEGER NOT NULL,
            id_accessoire INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            FOREIGN KEY (id_placard) REFERENCES Placard(id),
            FOREIGN KEY (id_accessoire) REFERENCES Accessoire(id)
        )
    """)

    # Insertion de données de test
    print("Création des données de test...")

    # Cuisines
    cur.execute("INSERT INTO Cuisine (nom, superficie, emplacement) VALUES (?, ?, ?)",
                ("Cuisine Moderne", 15.5, "Appartement Paris"))
    cur.execute("INSERT INTO Cuisine (nom, superficie, emplacement) VALUES (?, ?, ?)",
                ("Cuisine Classique", 12.0, "Maison Lyon"))
    cur.execute("INSERT INTO Cuisine (nom, superficie, emplacement) VALUES (?, ?, ?)",
                ("Cuisine Industrielle", 20.0, "Loft Marseille"))

    # Accessoires
    accessoires = [
        ("Poignée inox", "Quincaillerie", 5.50),
        ("Charnière", "Quincaillerie", 3.20),
        ("Étagère en verre", "Rangement", 15.00),
        ("Tiroir coulissant", "Rangement", 25.00),
        ("Éclairage LED", "Électrique", 12.00),
        ("Rail de tiroir", "Quincaillerie", 8.50)
    ]

    for acc in accessoires:
        cur.execute("INSERT INTO Accessoire (nom, categorie, prix_unitaire) VALUES (?, ?, ?)", acc)

    # Placards pour Cuisine 1
    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, "Haut", 80, 70, 35, "Blanc"))
    placard1_id = cur.lastrowid

    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, "Bas", 80, 85, 60, "Blanc"))
    placard2_id = cur.lastrowid

    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (1, "Colonne", 60, 200, 60, "Gris"))
    placard3_id = cur.lastrowid

    # Placards pour Cuisine 2
    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (2, "Haut", 60, 70, 35, "Bois"))
    placard4_id = cur.lastrowid

    cur.execute("""
        INSERT INTO Placard (id_cuisine, type, largeur, hauteur, profondeur, couleur)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (2, "Bas", 120, 85, 60, "Bois"))
    placard5_id = cur.lastrowid

    # Associations Placard-Accessoire
    associations = [
        (placard1_id, 1, 2),  # 2 poignées
        (placard1_id, 2, 4),  # 4 charnières
        (placard1_id, 3, 2),  # 2 étagères
        (placard2_id, 1, 2),
        (placard2_id, 4, 1),  # 1 tiroir
        (placard2_id, 6, 2),  # 2 rails
        (placard3_id, 1, 1),
        (placard3_id, 5, 2),  # 2 LED
        (placard4_id, 1, 2),
        (placard4_id, 2, 4),
        (placard5_id, 1, 3),
        (placard5_id, 4, 2),
    ]

    for assoc in associations:
        cur.execute("""
            INSERT INTO Placard_Accessoire (id_placard, id_accessoire, quantite)
            VALUES (?, ?, ?)
        """, assoc)

    conn.commit()
    conn.close()

    print("✅ Base de données initialisée avec succès !")
    print("📁 Fichier : data/kitchen.db")

if __name__ == "__main__":
    init_database()
