import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SÉCURITÉ ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Veuillez vous connecter sur l'accueil.")
    st.stop()

st.title("📊 Exploration des Données")

try:
    df = pd.read_csv("data/insurance_data.csv")

    # --- 2. FILTRES ACCESSIBLES ---
    st.subheader("🔍 Filtres de recherche")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        region_filter = st.multiselect(
            label="Filtrer par région géographique :",
            options=df['region'].unique(),
            default=df['region'].unique(),
            help="Sélectionnez les régions. Navigation clavier via TAB."
        )
    
    with col_f2:
        smoker_filter = st.radio(
            label="Filtrer par statut tabagique :",
            options=["Tous", "yes", "no"],
            horizontal=True,
            help="Comparez les profils fumeurs et non-fumeurs."
        )

    # Application des filtres
    df_filtered = df[df['region'].isin(region_filter)]
    if smoker_filter != "Tous":
        df_filtered = df_filtered[df_filtered['smoker'] == smoker_filter]

    st.divider()

    # --- 3. APERÇU ---
    st.write(f"Affichage de **{len(df_filtered)}** profils correspondants :")
    st.dataframe(df_filtered.head())
    
    # --- 4. ANALYSE PAR CATÉGORIE (Boxplot) ---
    st.subheader("Analyse des frais par catégorie")
    var = st.selectbox(
        label="Comparer les frais selon :",
        options=["sex", "smoker", "region"]
    )
    fig_box = px.box(df_filtered, x=var, y="charges", color=var, title=f"Frais selon : {var}")
    st.plotly_chart(fig_box)

    st.divider()

    # --- 5. TON ANCIEN DASHBOARD DE CORRÉLATION (BULLES) ---
    st.subheader("🎯 Dashboard Interactif : Âge, IMC et Frais")
    st.write("""
    Ce graphique montre l'impact combiné de l'Âge et de l'IMC. 
    **La taille et la couleur des bulles représentent le montant des frais.**
    """)

    fig_corr = px.scatter(
        df_filtered, 
        x="age", 
        y="bmi", 
        size="charges",      
        color="charges",     
        hover_name="id_client", 
        labels={
            "age": "Âge de l'assuré",
            "bmi": "Indice de Masse Corporelle (IMC)",
            "charges": "Frais Médicaux (€)"
        },
        title="Corrélation multidimensionnelle : Âge vs IMC (Bulles = Frais)",
        color_continuous_scale=px.colors.sequential.Plasma # Couleurs contrastées
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # --- 6. NOTE ACCESSIBILITÉ ---
    st.info("""
    **♿ Mesures d'accessibilité implémentées :**
    - **Navigation** : Tous les filtres sont accessibles via la touche **TAB**.
    - **Labels explicites** : Chaque menu possède un libellé clair pour les lecteurs d'écran.
    - **Interactivité** : Le graphique permet un survol détaillé (Hover) pour pallier les difficultés visuelles.
    """)

except Exception as e:
    st.error(f"Erreur : {e}")
