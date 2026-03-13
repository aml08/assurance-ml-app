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

# --- ANALYSE DES BIAIS
st.divider()
st.subheader("⚖️ Analyse d'équité et Atténuation des biais")

# On calcule l'erreur moyenne pour les fumeurs vs non-fumeurs
df_test = X_test.copy()
df_test['actual'] = y_test
df_test['pred'] = model.predict(X_test)
df_test['erreur'] = df_test['pred'] - df_test['actual']

# Affichage des erreurs moyennes par catégorie (ex: Smoker)
# Note: 1 = Yes, 0 = No (selon ton LabelEncoder)
bias_analysis = df_test.groupby('smoker')['erreur'].mean()
st.write("**Erreur moyenne de prédiction par catégorie (Fumeur vs Non-Fumeur) :**")
st.bar_chart(bias_analysis)

st.warning("""
**Analyse des biais :** Si l'erreur est beaucoup plus élevée pour les fumeurs, le modèle "sur-pénalise" cette catégorie. 
Cela peut être dû à un déséquilibre dans les données (pas assez d'exemples de fumeurs en bonne santé).
""")

st.info("""
**Solutions proposées pour atténuer les biais :**
1. **Rééquilibrage (Oversampling) :** Ajouter des données synthétiques pour les catégories sous-représentées.
2. **Contrainte d'Équité (Fairness constraints) :** Ajuster le modèle pour minimiser la différence d'erreur entre les groupes.
3. **Audit des variables :** Vérifier si la 'région' n'est pas un proxy masqué pour une discrimination sociale.
""")
