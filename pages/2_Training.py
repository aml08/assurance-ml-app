import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 1. SÉCURITÉ
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.stop()

st.title("⚙️ Entraînement du Modèle")

try:
    # 2. CHARGEMENT
    df = pd.read_csv("data/insurance_data.csv")
    
    if st.button("Lancer l'entraînement"):
        with st.spinner('Entraînement de l\'IA en cours...'):
            # 3. PRÉPARATION (Preprocessing)
            le = LabelEncoder()
            df['sex'] = le.fit_transform(df['sex'])
            df['smoker'] = le.fit_transform(df['smoker'])
            df['region'] = le.fit_transform(df['region'])
            
            X = df.drop('charges', axis=1)
            y = df['charges']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # 4. MODÈLE
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # 5. RÉSULTATS
            score = model.score(X_test, y_test)
            st.success(f"Modèle entraîné avec succès !")
            st.metric("Précision du modèle (R²)", f"{score:.2%}")
            
            # LOGS
            print(f"LOG: Modèle Assurance entraîné - Score: {score}")
            
except Exception as e:
    st.error(f"Erreur : {e}")