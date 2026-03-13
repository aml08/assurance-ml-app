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
            # 1. Sélectionner uniquement les colonnes utiles
            features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
            df_ml = df[features].copy()
            
            # 2. Transformer le texte en nombres (Encoding)
            le = LabelEncoder()
            df_ml['sex'] = le.fit_transform(df_ml['sex'])
            df_ml['smoker'] = le.fit_transform(df_ml['smoker'])
            df_ml['region'] = le.fit_transform(df_ml['region'])
            
            # 3. Séparer les caractéristiques (X) de la cible (y)
            X = df_ml.drop('charges', axis=1)
            y = df_ml['charges']
            
            # 4. Découper en train/test
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # 5. Entraîner le modèle
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # 6. Afficher les résultats
            score = model.score(X_test, y_test)
            st.success(f"Modèle entraîné avec succès !")
            st.metric("Précision (R²)", f"{score:.2%}")
            
except Exception as e:
    st.error(f"Erreur : {e}")
