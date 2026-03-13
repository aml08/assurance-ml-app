import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. VÉRIFICATION DE L'ACCÈS ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Veuillez vous connecter sur la page d'accueil pour accéder aux données.")
    st.stop()

# --- 2. CHARGEMENT DES DONNÉES ---
st.title("📊 Exploration & Analyse des Données")

@st.cache_data # Pour éviter de recharger le fichier à chaque clic
def load_data():
    df = pd.read_csv("data/insurance_data.csv")
    return df

try:
    df = load_data()

    # --- 3. APERÇU GÉNÉRAL ---
    st.subheader("📋 Aperçu du Dataset")
    st.write(f"Le jeu de données contient **{df.shape[0]}** entrées et **{df.shape[1]}** colonnes.")
    
    # Affichage des premières lignes
    with st.expander("Voir les données brutes"):
        st.dataframe(df.head(10))

    # Statistiques rapides
    col1, col2, col3 = st.columns(3)
    col1.metric("Âge moyen", f"{df['age'].mean():.1f} ans")
    col2.metric("IMC moyen", f"{df['bmi'].mean():.1f}")
    col3.metric("Frais moyens", f"{df['charges'].mean():,.0f} €")

    st.divider()

    # --- 4. DASHBOARD INTERACTIF DE CORRÉLATION ---
    st.subheader("🎯 Dashboard de Corrélation : Âge, IMC et Frais")
    
    st.write("""
    Ce graphique interactif permet d'analyser la relation entre les trois facteurs principaux. 
    Utilisez les outils de survol pour voir les détails de chaque profil.
    """)

    # Création du Scatter Plot (Âge vs IMC avec Frais en couleur/taille)
    fig_corr = px.scatter(
        df, 
        x="age", 
        y="bmi", 
        size="charges",      # La taille du point varie selon les frais
        color="charges",     # La couleur varie selon les frais
        hover_name="id_client", 
        hover_data=['smoker', 'region_fr'],
        labels={
            "age": "Âge de l'assuré",
            "bmi": "Indice de Masse Corporelle (IMC)",
            "charges": "Frais Médicaux (€)"
        },
        title="Impact de l'Âge et de l'IMC sur les Frais d'Assurance",
        color_continuous_scale=px.colors.sequential.Plasma,
        template="plotly_white"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    st.info("""
    **Analyse :** On observe une corrélation positive : les frais ont tendance à augmenter (points plus gros et plus clairs) 
    à mesure que l'âge et l'IMC progressent simultanément.
    """)

    # --- 5. ANALYSE PAR CATÉGORIE ---
    st.divider()
    st.subheader("🚬 Impact du Tabagisme")
    
    fig_box = px.box(
        df, 
        x="smoker", 
        y="charges", 
        color="smoker",
        notched=True,
        title="Répartition des frais : Fumeurs vs Non-Fumeurs",
        labels={"smoker": "Fumeur", "charges": "Frais (€)"}
    )
    st.plotly_chart(fig_box)

except FileNotFoundError:
    st.error("❌ Erreur : Le fichier 'data/insurance_data.csv' est introuvable. Vérifiez votre dossier 'data' sur GitHub.")
except Exception as e:
    st.error(f"❌ Une erreur est survenue : {e}")

# --- PIED DE PAGE ---
st.sidebar.markdown("---")
st.sidebar.info("Données synchronisées avec le dépôt GitHub.")
