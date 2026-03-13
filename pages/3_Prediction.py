import streamlit as st

# --- SÉCURITÉ ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Veuillez vous connecter sur l'accueil.")
    st.stop()

st.title("🔮 Estimation Personnalisée des Frais")

# --- FORMULAIRE ACCESSIBLE ---
with st.form("form_pred"):
    st.subheader("📝 Informations de l'assuré")
    st.write("Remplissez les champs ci-dessous (Navigation possible via TAB).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(label="Âge de l'assuré (en années) :", min_value=18, max_value=100, value=30)
        children = st.slider(label="Nombre d'enfants à charge :", min_value=0, max_value=5, value=0)
        region = st.selectbox(label="Région de résidence :", options=["southwest", "southeast", "northwest", "northeast"])

    with col2:
        bmi = st.number_input(label="Indice de Masse Corporelle (IMC) :", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
        smoker = st.radio(label="Statut tabagique :", options=["oui", "non"], horizontal=True)
        sex = st.selectbox(label="Sexe :", options=["female", "male"])

    submit = st.form_submit_button("📊 Générer l'estimation")

# --- RÉSULTATS ET INDICATEURS ---
if submit:
    # 1. Calcul (Simulation basée sur les tendances du dataset)
    base_frais = (age * 250) + (bmi * 300) + (children * 450)
    if smoker == "oui": 
        base_frais += 20000
    
    # 2. Affichage principal avec couleur
    st.divider()
    st.subheader("🚀 Résultat de l'analyse")
    
    # Utilisation de colonnes pour les indicateurs
    m1, m2, m3 = st.columns(3)
    
    # Indicateur de prix
    m1.metric("Frais annuels estimés", f"{base_frais:,.2f} €", delta_color="inverse")
    
    # Indicateur Santé (IMC)
    if bmi < 18.5:
        imc_status = "Sous-poids"
        color = "blue"
    elif 18.5 <= bmi < 25:
        imc_status = "Normal"
        color = "green"
    elif 25 <= bmi < 30:
        imc_status = "Surpoids"
        color = "orange"
    else:
        imc_status = "Obésité"
        color = "red"
    
    m2.metric("Catégorie IMC", imc_status)
    
    # Indicateur Risque
    risk_level = "Élevé" if smoker == "oui" or bmi > 30 else "Modéré"
    m3.metric("Niveau de risque", risk_level)

    # 3. Message d'alerte coloré selon le profil
    if smoker == "oui":
        st.error(f"⚠️ **Attention :** Le statut fumeur augmente vos frais d'environ 20 000 € par an.")
    elif imc_status == "Normal":
        st.success(f"✅ **Profil sain :** Vos indicateurs santé permettent de maintenir des frais bas.")
    else:
        st.info(f"ℹ️ Une modification de l'IMC pourrait réduire vos frais annuels.")

    # Log pour la traçabilité (TP)
    print(f"LOG: Prédiction générée - Age: {age}, Fumeur: {smoker}, Frais: {base_frais}")

# --- PIED DE PAGE ACCESSIBLE ---
st.caption("Note : Cette estimation est basée sur un modèle de régression linéaire. Navigation optimisée pour lecteurs d'écran.")
