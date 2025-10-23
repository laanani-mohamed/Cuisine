import streamlit as st
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.forms import render_add_cuisine_form, render_add_placard_form

# Configuration de la page
st.set_page_config(
    page_title="Kitchen Manager",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Afficher la sidebar et récupérer la cuisine sélectionnée
    cuisine_id = render_sidebar()

    # Créer des onglets
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Ajouter Cuisine", "➕ Ajouter Placard"])

    with tab1:
        render_dashboard(cuisine_id)

    with tab2:
        render_add_cuisine_form()

    with tab3:
        render_add_placard_form(cuisine_id)

if __name__ == "__main__":
    main()
