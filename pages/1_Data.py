import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SÉCURITÉ ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("Veuillez vous connecter sur l'accueil.")
    st.stop()

st.title("📊 Exploration des Données")

try:
    # --- 2. CHARGEMENT ET APERÇU (Ce que tu avais de base) ---
    df = pd.read_csv("data/insurance_data.csv")
    st.write("Aperçu des données :")
    st.dataframe(df.head())
    
    # --- 3. PREMIER GRAPHIQUE (Ce que tu avais de base) ---
    st.subheader("Analyse des frais par catégorie")
    var = st.selectbox("Choisir une variable pour le boxplot", ["sex", "smoker", "region"])
    fig_box = px.box(df, x=var, y="charges", color=var, title=f"Frais selon : {var}")
    st.plotly_chart(fig_box)

    st.divider()

    # --- 4. LE NOUVEAU DASHBOARD (Ajout demandé) ---
    st.subheader("🎯 Dashboard Interactif : Corrélation Âge, IMC et Frais")
    st.write("""
    Ce graphique montre comment l'âge et l'IMC influencent conjointement les frais. 
    **La taille et la couleur des points représentent le montant des frais.**
    """)

    fig_corr = px.scatter(
        df, 
        x="age", 
        y="bmi", 
        size="charges",      
        color="charges",     
        hover_name="id_client", 
        labels={
            "age": "Âge",
            "bmi": "IMC (BMI)",
            "charges": "Frais (€)"
        },
        title="Corrélation multidimensionnelle : Âge vs IMC vs Frais",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.info("💡 Plus les points sont gros et jaunes, plus le profil est coûteux pour l'assurance.")

except Exception as e:
    st.error(f"Erreur de chargement : {e}")
