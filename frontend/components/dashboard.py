import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"

def render_dashboard(cuisine_id):
    """Affiche le dashboard principal pour une cuisine"""

    if not cuisine_id:
        st.info("👈 Sélectionnez une cuisine dans la barre latérale")
        return

    # Récupérer les infos de la cuisine
    try:
        response = requests.get(f"{API_URL}/cuisines/{cuisine_id}")
        if response.status_code == 200:
            cuisine = response.json()

            # En-tête
            st.title(f"📊 {cuisine['nom']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Superficie", f"{cuisine['superficie']} m²")
            with col2:
                st.metric("Emplacement", cuisine['emplacement'])

            st.markdown("---")

            # Section analyse des coûts
            st.subheader("💰 Analyse des coûts")

            if st.button("Calculer le coût total", type="primary"):
                response_cout = requests.get(f"{API_URL}/analyse/cout/{cuisine_id}")
                if response_cout.status_code == 200:
                    data = response_cout.json()
                    with col3:
                        st.metric("Coût Total", f"{data['cout_total']:.2f} €")

            # Afficher les placards
            st.markdown("---")
            st.subheader("🗄️ Placards de la cuisine")

            response_placards = requests.get(f"{API_URL}/placards/{cuisine_id}")
            if response_placards.status_code == 200:
                placards = response_placards.json()["placards"]

                if placards:
                    df_placards = pd.DataFrame(placards)
                    st.dataframe(
                        df_placards[['id', 'type', 'largeur', 'hauteur', 'profondeur', 'couleur']],
                        use_container_width=True
                    )
                else:
                    st.info("Aucun placard pour cette cuisine")

            # Section graphiques
            st.markdown("---")
            st.subheader("📈 Visualisations")

            col_graph1, col_graph2 = st.columns(2)

            with col_graph1:
                # Graphique coût par placard
                response_cout_placard = requests.get(f"{API_URL}/analyse/cout-par-placard/{cuisine_id}")
                if response_cout_placard.status_code == 200:
                    data_placards = response_cout_placard.json()["placards"]
                    if data_placards:
                        df_cout = pd.DataFrame(data_placards)
                        df_cout['cout_total'] = df_cout['cout_total'].fillna(0)

                        fig_bar = px.bar(
                            df_cout,
                            x='type',
                            y='cout_total',
                            color='couleur',
                            title="Coût par type de placard",
                            labels={'cout_total': 'Coût (€)', 'type': 'Type de placard'}
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

            with col_graph2:
                # Graphique répartition accessoires
                response_repartition = requests.get(f"{API_URL}/analyse/repartition-accessoires/{cuisine_id}")
                if response_repartition.status_code == 200:
                    data_rep = response_repartition.json()["repartition"]
                    if data_rep:
                        df_rep = pd.DataFrame(data_rep)

                        fig_pie = px.pie(
                            df_rep,
                            values='cout_total',
                            names='categorie',
                            title="Répartition des coûts par catégorie"
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)

        else:
            st.error("Impossible de charger les données de la cuisine")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Erreur de connexion à l'API")
