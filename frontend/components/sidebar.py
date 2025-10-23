import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def render_sidebar():
    """Affiche la sidebar avec les options de navigation"""

    with st.sidebar:
        st.title("🏠 Kitchen Manager")
        st.markdown("---")

        # Récupérer la liste des cuisines
        try:
            response = requests.get(f"{API_URL}/cuisines")
            if response.status_code == 200:
                cuisines = response.json()["cuisines"]

                if cuisines:
                    cuisine_options = {f"{c['nom']} (ID: {c['id']})": c['id']
                                      for c in cuisines}

                    selected = st.selectbox(
                        "Sélectionner une cuisine",
                        options=list(cuisine_options.keys())
                    )

                    cuisine_id = cuisine_options[selected]

                    return cuisine_id
                else:
                    st.warning("Aucune cuisine disponible")
                    return None
            else:
                st.error("Erreur de connexion à l'API")
                return None

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Impossible de se connecter à l'API")
            st.info("Assurez-vous que le backend est démarré avec: `uvicorn backend.app:app --reload`")
            return None
