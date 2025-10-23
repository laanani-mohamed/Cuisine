# 🏠 Kitchen Manager - Application de gestion de cuisines

Application complète permettant de gérer et analyser des données de cuisines, placards, compartiments et accessoires.

## 🧱 Architecture

- **Base de données** : SQLite locale
- **Backend** : FastAPI (Python)
- **Frontend** : Streamlit

## 📁 Structure du projet

```
kitchen_app/
│
├── backend/
│   ├── app.py           # Application FastAPI principale
│   ├── db.py            # Fonctions d'accès à la base de données
│   ├── models.py        # Modèles Pydantic
│   └── utils.py         # Fonctions utilitaires (calculs)
│
├── frontend/
│   ├── app.py           # Application Streamlit principale
│   └── components/
│       ├── sidebar.py   # Barre latérale
│       ├── dashboard.py # Tableau de bord
│       └── forms.py     # Formulaires d'ajout
│
├── data/
│   └── kitchen.db       # Base de données SQLite (créée après init)
│
├── init_db.py           # Script d'initialisation de la BDD
├── requirements.txt     # Dépendances Python
└── README.md
```

## 🚀 Installation et lancement

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
python init_db.py
```

Cette commande crée la base de données `data/kitchen.db` avec des données de test.

### 3. Démarrer le backend

Ouvrez un premier terminal :

```bash
cd backend
uvicorn app:app --reload
```

Le backend sera accessible sur : http://127.0.0.1:8000

Documentation API interactive : http://127.0.0.1:8000/docs

### 4. Démarrer le frontend

Ouvrez un second terminal :

```bash
cd frontend
streamlit run app.py
```

L'interface utilisateur sera accessible sur : http://localhost:8501

## 📊 Fonctionnalités

### Backend (API REST)

- `GET /cuisines` - Liste de toutes les cuisines
- `GET /cuisines/{id}` - Détails d'une cuisine
- `GET /placards/{id_cuisine}` - Placards d'une cuisine
- `POST /placard` - Ajouter un placard
- `POST /cuisine` - Ajouter une cuisine
- `GET /analyse/cout/{id_cuisine}` - Calcul du coût total
- `GET /analyse/cout-par-placard/{id_cuisine}` - Coût par placard
- `GET /analyse/repartition-accessoires/{id_cuisine}` - Répartition des accessoires
- `GET /accessoires` - Liste des accessoires

### Frontend (Interface Streamlit)

- **Dashboard** :
  - Sélection d'une cuisine
  - Affichage des informations (superficie, emplacement)
  - Calcul du coût total
  - Liste des placards
  - Graphiques :
    - Coût par type de placard (bar chart)
    - Répartition des accessoires (pie chart)

- **Formulaires** :
  - Ajouter une nouvelle cuisine
  - Ajouter un nouveau placard

## 🗃️ Schéma de base de données

```sql
Cuisine
├── id (PK)
├── nom
├── superficie
└── emplacement

Placard
├── id (PK)
├── id_cuisine (FK)
├── type
├── largeur
├── hauteur
├── profondeur
└── couleur

Compartiment
├── id (PK)
├── id_placard (FK)
├── type
├── hauteur
├── largeur
└── profondeur

Accessoire
├── id (PK)
├── nom
├── categorie
└── prix_unitaire

Placard_Accessoire
├── id (PK)
├── id_placard (FK)
├── id_accessoire (FK)
└── quantite
```

## 💡 Exemple d'utilisation

1. Lancez le backend et le frontend
2. Sélectionnez une cuisine dans la barre latérale
3. Cliquez sur "Calculer le coût total" pour voir le prix
4. Consultez les graphiques pour analyser la répartition des coûts
5. Utilisez les onglets pour ajouter de nouvelles cuisines ou placards

## 🛠️ Technologies utilisées

- **Python 3.x**
- **FastAPI** - Framework web moderne et rapide
- **Streamlit** - Framework pour créer des interfaces de data science
- **SQLite** - Base de données légère
- **Pandas** - Manipulation de données
- **Plotly** - Graphiques interactifs
- **Pydantic** - Validation de données

## 📝 Notes

- Le backend doit être démarré avant le frontend
- La base de données est créée automatiquement avec des données de test
- L'API est documentée automatiquement via Swagger UI (/docs)

## 🎯 Prochaines améliorations possibles

- Export des données (PDF, Excel)
- Authentification utilisateur
- Upload d'images pour les cuisines
- Gestion des compartiments
- Historique des modifications
- Tests unitaires et d'intégration