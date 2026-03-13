import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SÉCURITÉ ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Veuillez vous connecter sur l'accueil.")
    st.stop()

st.title("📊 Exploration & Filtres Accessibles")

try:
    df = pd.read_csv("data/insurance_data.csv")

    # --- 2. SECTION FILTRES (Accessibilité : Libellés explicites) ---
    st.subheader("🔍 Filtrer les données")
    st.write("Utilisez les menus ci-dessous pour segmenter le tableau (Navigation possible via la touche TAB).")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        # Label explicite pour lecteur d'écran
        region_filter = st.multiselect(
            label="Filtrer par région géographique :",
            options=df['region'].unique(),
            default=df['region'].unique(),
            help="Sélectionnez une ou plusieurs régions pour mettre à jour les graphiques."
        )
    
    with col_f2:
        smoker_filter = st.radio(
            label="Statut tabagique :",
            options=["Tous", "yes", "no"],
            horizontal=True,
            help="Choisissez d'afficher uniquement les fumeurs, les non-fumeurs ou tout le monde."
        )
        
    with col_f3:
        # Filtre par âge avec un slider accessible
        age_min, age_max = int(df['age'].min()), int(df['age'].max())
        age_range = st.slider(
            label="Tranche d'âge des assurés :",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max)
        )

    # Application des filtres au dataframe
    df_filtered = df[df['region'].isin(region_filter)]
    if smoker_filter != "Tous":
        df_filtered = df_filtered[df_filtered['smoker'] == smoker_filter]
    df_filtered = df_filtered[(df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1])]

    # --- 3. AFFICHAGE DU TABLEAU ---
    st.write(f"Affichage de **{len(df_filtered)}** profils correspondants :")
    st.dataframe(df_filtered.head(50), use_container_width=True)

    st.divider()

    # --- 4. GRAPHISMES À HAUT CONTRASTE ---
    st.subheader("🎯 Analyse visuelle (Contraste élevé)")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Heatmap avec palette de couleurs contrastées (RdBu_r est excellent pour l'accessibilité)
        st.write("**Matrice de corrélations numériques**")
        corr = df_filtered[['age', 'bmi', 'children', 'charges']].corr()
        fig_heat = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale='RdBu_r', # Bleu et Rouge contrastés
            labels=dict(color="Force du lien")
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with c2:
        # Graphique de tendance avec une ligne rouge vive sur fond blanc
        st.write("**Évolution des frais par âge**")
        fig_trend = px.scatter(
            df_filtered, x="age", y="charges", 
            color_discrete_sequence=['#00441b'], # Vert très foncé pour le contraste
            trendline="ols",
            trendline_color_override="#e31a1c", # Rouge vif pour la visibilité
            labels={"age": "Âge (années)", "charges": "Frais (€)"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # --- 5. NOTE D'ACCESSIBILITÉ ---
    with st.expander("♿ Note sur l'accessibilité de cette page"):
        st.markdown("""
        * **Contraste** : Les palettes de couleurs Plotly ('RdBu_r') ont été choisies pour rester lisibles même en cas de daltonisme.
        * **Navigation** : Tous les filtres ci-dessus sont utilisables au clavier (Tab + Flèches/Entrée).
        * **Labels** : Chaque champ possède un `label` explicite plutôt qu'un simple placeholder, facilitant l'usage des lecteurs d'écran.
        """)

except Exception as e:
    st.error(f"Erreur : {e}")
