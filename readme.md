# 🏥 Système Expert de Prédiction d'Assurance Santé

Ce projet est une application web interactive de Data Science développée avec **Streamlit**. Elle permet d'explorer des données d'assurance, d'entraîner un modèle de Machine Learning et de prédire les frais médicaux annuels d'un assuré.

##  Fonctionnalités principales

L'application est divisée en trois modules clés :
1. **Data Exploration** : Visualisation interactive du dataset, analyse des corrélations (Heatmap) et impact des variables (Âge, IMC, Tabac) sur les coûts.
2. **Modélisation** : Entraînement d'un modèle de **Régression Linéaire** avec affichage des coefficients pour garantir l'explicabilité de l'IA.
3. **Prédiction** : Interface de saisie utilisateur avec validation des entrées pour estimer les frais en temps réel.

##  Sécurité et Conformité

Cette application intègre des mesures de sécurité robustes :
* **Authentification** : Accès protégé par un mot de passe sécurisé via `st.secrets`.
* **RGPD** : Mise en place d'une notice de consentement et d'une politique de confidentialité à l'entrée.
* **Gestion des Logs** : Traçabilité complète des événements (connexions, erreurs, entraînements) consultable dans la console d'administration.
* **Validation des entrées** : Utilisation de bornes numériques (min/max) pour empêcher l'injection de données incohérentes.
* **HTTPS** : Déploiement sécurisé avec chiffrement SSL sur Streamlit Cloud.

##  Structure du Projet

```text
├── app.py                # Page d'accueil, Sécurité et RGPD
├── requirements.txt      # Dépendances Python
├── data/
│   └── insurance_data.csv # Dataset source
├── pages/
│   ├── 1_Data.py         # Visualisation et Dashboards
│   ├── 2_Training.py     # Entraînement et Coefficients
│   └── 3_Prediction.py   # Formulaire de prédiction
└── utils/

    └── model_utils.py    # Fonctions de nettoyage

1. Clôner le depôt
git clone [https://github.com/votre-pseudo/assurance-ml-app.git](https://github.com/votre-pseudo/assurance-ml-app.git)

2. Installer les dépendances
pip install -r requirements.txt

3. Lancer l'application
streamlit run app.py

## Accès Direct (Démo en ligne)

L'application est déployée et accessible ici : 
https://assurance-ml-app-aml08.streamlit.app
Utilisateur : admin
Mdp : admin



