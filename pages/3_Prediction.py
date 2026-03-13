import streamlit as st

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.stop()

st.title("🔮 Estimation des Frais")

with st.form("form_pred"):
    age = st.number_input("Âge", 18, 100, 30)
    bmi = st.number_input("IMC (BMI)", 10.0, 60.0, 25.0)
    children = st.slider("Enfants", 0, 5, 0)
    smoker = st.selectbox("Fumeur", ["yes", "no"])
    submit = st.form_submit_button("Calculer")

if submit:
    # Calcul simplifié pour vérifier que l'interface marche
    frais = (age * 100) + (bmi * 50) + (children * 500)
    if smoker == "yes": frais += 15000
    
    st.metric("Frais annuels estimés", f"{frais:,.2f} €")
    print(f"LOG: Prédiction pour âge {age}")