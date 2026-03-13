import streamlit as st

st.set_page_config(page_title="Assurance Predict", page_icon="🏥")

# Sécurité
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if pwd == st.secrets["PASSWORD"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Accès refusé")

if not st.session_state["authenticated"]:
    st.title("🔐 Accès Restreint")
    login()
    st.stop()

st.title("🏥 Système Expert Assurance")
st.success("Connexion réussie !")
st.write("Bienvenue. Utilisez le menu à gauche pour explorer les données ou prédire des frais.")