import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression # On change le modèle ici
from sklearn.preprocessing import LabelEncoder

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.stop()

st.title("⚙️ Entraînement & Interprétation")

try:
    df = pd.read_csv("data/insurance_data.csv")
    
    if st.button("Lancer l'entraînement du modèle"):
        with st.spinner('Analyse mathématique en cours...'):
            # 1. Préparation (identique)
            features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
            df_ml = df[features].copy()
            
            le = LabelEncoder()
            for col in ['sex', 'smoker', 'region']:
                df_ml[col] = le.fit_transform(df_ml[col])
            
            X = df_ml.drop('charges', axis=1)
            y = df_ml['charges']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # 2. Modèle de Régression Linéaire
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # 3. Affichage des résultats
            score = model.score(X_test, y_test)
            st.success("Modèle entraîné !")
            st.metric("Score de précision (R²)", f"{score:.2%}")

            # --- PARTIE EXPLICATION DES COEFFICIENTS ---
            st.subheader("💡 Interprétation du modèle")
            st.write("""
            Le modèle de **Régression Linéaire** cherche à créer une équation où chaque caractéristique 
            (âge, IMC, tabac) a un poids appelé **Coefficient**. 
            Plus le coefficient est élevé, plus la caractéristique impacte le prix final.
            """)
            
            # Création d'un tableau pour les coefficients
            coeff_df = pd.DataFrame({
                'Caractéristique': X.columns,
                'Influence (Coefficient)': model.coef_
            }).sort_values(by='Influence (Coefficient)', ascending=False)
            
            st.table(coeff_df)
            
            st.info("""
            **Comment lire ce tableau ?** Par exemple, si le coefficient du 'smoker' est très élevé, cela signifie que le fait de fumer 
            ajoute directement ce montant au prix de l'assurance.
            """)

except Exception as e:
    st.error(f"Erreur : {e}")

# --- ANALYSE RÉELLE DES BIAIS 
st.divider()
st.subheader("⚖️ Analyse factuelle de l'équité du modèle")

# Préparation des données de test pour l'analyse
df_test = X_test.copy()
df_test['Réel'] = y_test
df_test['Prédiction'] = model.predict(X_test)
df_test['Erreur_Absolue'] = abs(df_test['Prédiction'] - df_test['Réel'])

# 1. Observation factuelle sur le Tabagisme (Le biais le plus fort)
bias_smoker = df_test.groupby('smoker')['Erreur_Absolue'].mean()

st.write("### Constatations sur les données")
col1, col2 = st.columns(2)

with col1:
    st.write("**Erreur moyenne par statut :**")
    st.bar_chart(bias_smoker)

with col2:
    diff_erreur = bias_smoker.max() - bias_smoker.min()
    st.metric("Écart d'erreur (Biais)", f"{diff_erreur:,.2f} €")
