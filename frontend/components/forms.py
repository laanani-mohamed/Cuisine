import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def render_add_cuisine_form():
    """Affiche le formulaire d'ajout d'une cuisine"""

    st.subheader("➕ Ajouter une nouvelle cuisine")

    with st.form("form_cuisine"):
        nom = st.text_input("Nom de la cuisine", placeholder="Ex: Cuisine Moderne")
        superficie = st.number_input("Superficie (m²)", min_value=0.0, step=0.5)
        emplacement = st.text_input("Emplacement", placeholder="Ex: Appartement Paris")

        submitted = st.form_submit_button("Créer la cuisine")

        if submitted:
            if nom and superficie and emplacement:
                try:
                    response = requests.post(
                        f"{API_URL}/cuisine",
                        json={
                            "nom": nom,
                            "superficie": superficie,
                            "emplacement": emplacement
                        }
                    )

                    if response.status_code == 200:
                        st.success(f"✅ Cuisine '{nom}' créée avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Impossible de se connecter à l'API")
            else:
                st.warning("Veuillez remplir tous les champs")

def render_add_placard_form(cuisine_id):
    """Affiche le formulaire d'ajout d'un placard"""

    if not cuisine_id:
        st.info("Sélectionnez d'abord une cuisine")
        return

    st.subheader("➕ Ajouter un placard")

    with st.form("form_placard"):
        type_placard = st.selectbox(
            "Type de placard",
            ["Haut", "Bas", "Colonne", "Angle"]
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            largeur = st.number_input("Largeur (cm)", min_value=0.0, step=5.0)
        with col2:
            hauteur = st.number_input("Hauteur (cm)", min_value=0.0, step=5.0)
        with col3:
            profondeur = st.number_input("Profondeur (cm)", min_value=0.0, step=5.0)

        couleur = st.text_input("Couleur", placeholder="Ex: Blanc")

        submitted = st.form_submit_button("Ajouter le placard")

        if submitted:
            if largeur and hauteur and profondeur and couleur:
                try:
                    response = requests.post(
                        f"{API_URL}/placard",
                        json={
                            "id_cuisine": cuisine_id,
                            "type": type_placard,
                            "largeur": largeur,
                            "hauteur": hauteur,
                            "profondeur": profondeur,
                            "couleur": couleur
                        }
                    )

                    if response.status_code == 200:
                        st.success(f"✅ Placard {type_placard} ajouté avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de l'ajout")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Impossible de se connecter à l'API")
            else:
                st.warning("Veuillez remplir tous les champs")
