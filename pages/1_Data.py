import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SÉCURITÉ ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Veuillez vous connecter sur l'accueil.")
    st.stop()

st.title("📊 Exploration des Données")

try:
    df = pd.read_csv("data/insurance_data.csv")
    
    # --- 2. APERÇU DES DONNÉES ---
    st.write("Aperçu des données :")
    st.dataframe(df.head())
    
    st.divider()

    # --- 3. ANALYSE SIMPLE (Boxplot) ---
    st.subheader("Analyse par catégorie")
    var = st.selectbox("Comparer les frais selon :", ["sex", "smoker", "region"])
    fig_box = px.box(df, x=var, y="charges", color=var, points="all", title=f"Frais selon : {var}")
    st.plotly_chart(fig_box)

    st.divider()

    # --- 4. DASHBOARD DE CORRÉLATION SIMPLIFIÉ ---
    st.subheader("🎯 Dashboard de Corrélation (Lisible)")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Matrice de Corrélation**")
        # On ne garde que les colonnes numériques pour la corrélation
        corr = df[['age', 'bmi', 'children', 'charges']].corr()
        fig_heat = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale='RdBu_r', 
            aspect="auto",
            title="Force des liens (1 = lien total)"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.write("**Tendance : Âge vs Frais**")
        # Un graphique avec une ligne de tendance (Trendline) pour la lisibilité
        fig_trend = px.scatter(
            df, x="age", y="charges", 
            trendline="ols", # Ajoute la ligne de régression
            trendline_color_override="red",
            title="Plus l'âge monte, plus les frais montent"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.info("""
    **Comment lire ce dashboard ?**
    - **À gauche (Heatmap) :** Plus le carré est rouge/foncé, plus la corrélation est forte. 
    - **À droite (Tendance) :** La ligne rouge montre la direction générale. Si elle monte, la corrélation est positive.
    """)

except Exception as e:
    st.error(f"Erreur : {e}")
