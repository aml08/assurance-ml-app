import streamlit as st
import pandas as pd
import plotly.express as px

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.stop()

st.title("📊 Exploration des Données")

try:
    df = pd.read_csv("data/insurance_data.csv")
    st.write("Aperçu du dataset :")
    st.dataframe(df.head())
    
    st.subheader("Analyse des frais par catégorie")
    var = st.selectbox("Choisir une variable", ["sex", "smoker", "region"])
    fig = px.box(df, x=var, y="charges", color=var, title=f"Frais selon : {var}")
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Erreur de chargement : {e}")