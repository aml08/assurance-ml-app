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

    # --- 2. AJOUT : FILTRES ACCESSIBLES (Nouveau) ---
    st.subheader("🔍 Filtres de recherche")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        # Label explicite pour l'accessibilité
        region_filter = st.multiselect(
            label="Filtrer par région géographique :",
            options=df['region'].unique(),
            default=df['region'].unique(),
            help="Sélectionnez les régions à afficher. Navigation clavier disponible (TAB)."
        )
    
    with col_f2:
        smoker_filter = st.radio(
            label="Filtrer par statut tabagique :",
            options=["Tous", "yes", "no"],
            horizontal=True,
            help="Filtre exclusif pour comparer les profils fumeurs/non-fumeurs."
        )

    # Application des filtres
    df_filtered = df[df['region'].isin(region_filter)]
    if smoker_filter != "Tous":
        df_filtered = df_filtered[df_filtered['smoker'] == smoker_filter]

    st.divider()

    # --- 3. APERÇU (Ce que tu avais de base) ---
    st.write(f"Affichage de **{len(df_filtered)}** lignes après filtrage :")
    st.dataframe(df_filtered.head())
    
    # --- 4. ANALYSE PAR CATÉGORIE (Ce que tu avais de base) ---
    st.subheader("Analyse des frais par catégorie")
    var = st.selectbox(
        label="Comparer les frais selon la variable suivante :", # Label explicite
        options=["sex", "smoker", "region"]
    )
    fig_box = px.box(df_filtered, x=var, y="charges", color=var, title=f"Frais selon : {var}")
    st.plotly_chart(fig_box)

    st.divider()

    # --- 5. DASHBOARD DE CORRÉLATION (Ce que tu avais de base) ---
    st.subheader("🎯 Dashboard de Corrélation")
    
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Matrice de Corrélation (Couleurs contrastées)**")
        corr = df_filtered[['age', 'bmi', 'children', 'charges']].corr()
        fig_heat = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale='RdBu_r', # Haut contraste (Bleu/Rouge)
            title="Force des liens"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.write("**Tendance : Âge vs Frais**")
        fig_trend = px.scatter(
            df_filtered, x="age", y="charges", 
            trendline="ols", 
            trendline_color_override="red", # Visibilité maximale
            title="Progression des frais"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # --- 6. AJOUT : NOTE ACCESSIBILITÉ (Nouveau) ---
    st.info("""
    **♿ Mesures d'accessibilité implémentées :**
    - **Navigation au clavier** : Tous les filtres sont accessibles via la touche **TAB**.
    - **Labels explicites** : Chaque menu possède un libellé clair pour les lecteurs d'écran.
    - **Contraste** : Utilisation de palettes de couleurs à haut contraste (Rouge/Bleu/Blanc).
    """)

except Exception as e:
    st.error(f"Erreur : {e}")
