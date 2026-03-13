import streamlit as st
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Assurance Predict - Sécurisé", page_icon="🏥")

# --- 1. GESTION DES LOGS (Fonction interne) ---
def log_event(message):
    """Affiche un log dans la console Streamlit Cloud (Manage App)"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] LOG: {message}")

# --- 2. GESTION DU CONSENTEMENT RGPD ---
if "rgpd_consent" not in st.session_state:
    st.session_state["rgpd_consent"] = False

if not st.session_state["rgpd_consent"]:
    st.title("🛡️ Protection de vos données")
    st.info("""
    **Notice RGPD / Privacy :** Cette application utilise des cookies de session pour l'authentification. 
    Les données saisies dans le formulaire de prédiction ne sont pas stockées de façon permanente. 
    En cliquant sur 'Accepter', vous consentez à l'utilisation de ces outils techniques.
    """)
    if st.button("Accepter et continuer"):
        st.session_state["rgpd_consent"] = True
        log_event("Consentement RGPD accepté par l'utilisateur.")
        st.rerun()
    st.stop()

# --- 3. GESTION DES ACCÈS (AUTHENTIFICATION) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 Accès Restreint")
    
    # Ajout du champ Nom d'utilisateur
    username = st.text_input("Identifiant")
    pwd = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        # On vérifie l'identifiant ET le mot de passe
        # Tu peux changer "admin" par le nom que tu veux
        if username == "admin" and pwd == st.secrets["PASSWORD"]:
            st.session_state["authenticated"] = True
            log_event(f"Authentification réussie pour l'utilisateur : {username}")
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect.")
            log_event(f"Échec d'authentification pour : {username}")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# --- 4. CONTENU DE L'APPLICATION (Une fois authentifié) ---
st.title("🏥 Système Expert Assurance")
st.success("Bienvenue dans l'interface sécurisée.")

st.markdown("""
### Présentation du projet
Cette plateforme permet d'estimer les frais d'assurance santé à partir de données anonymisées.
- **Conformité :** Application sécurisée via HTTPS.
- **Traçabilité :** Les accès et prédictions sont logués.
- **Navigation :** Utilisez la barre latérale pour explorer les données ou lancer l'IA.
""")

log_event("Page d'accueil consultée.")
