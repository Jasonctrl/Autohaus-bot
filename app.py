import streamlit as st
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# 🔐 API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Kein API Key gefunden!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# 🎨 UI
st.set_page_config(page_title="Audi Verkaufsassistent", page_icon="🚗")
st.title("🚗 Audi Verkaufsassistent")

# 💬 Speicher
if "messages" not in st.session_state:
    st.session_state.messages = []

if "leads" not in st.session_state:
    st.session_state.leads = []

# 🚗 Fahrzeugliste
cars = [
    {"name": "Audi A3", "price": 30000, "type": "Kompakt"},
    {"name": "Audi A4", "price": 40000, "type": "Limousine"},
    {"name": "Audi A6", "price": 55000, "type": "Premium"},
    {"name": "Audi Q3", "price": 38000, "type": "SUV"},
    {"name": "Audi Q5", "price": 52000, "type": "SUV"},
    {"name": "Audi Q7", "price": 75000, "type": "SUV"},
]

# 📜 Chat anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🧑 Eingabe
prompt = st.chat_input("Wie kann ich Ihnen helfen?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 🔍 Analyse
    filtered_cars = cars
    extra = ""

    if "unter 30000" in prompt.lower():
        filtered_cars = [c for c in cars if c["price"] <= 30000]
        extra = "Budget bis 30.000€"

    elif "familie" in prompt.lower():
        filtered_cars = [c for c in cars if c["type"] in ["SUV"]]
        extra = "Familienfreundliche Fahrzeuge"

    # 🚗 Liste bauen
    car_text = ""
    for car in filtered_cars:
        car_text += f"- {car['name']} ({car['price']}€)\n"

    # 🤖 KI Antwort
    with st.chat_message("assistant"):
        with st.spinner("Denke nach..."):
            try:
                time.sleep(1)

                response = model.generate_content(f"""
Du bist ein professioneller Audi Verkaufsberater.

Dein Stil:
- hochwertig
- ruhig
- kompetent

Deine Aufgabe:
- Kunden beraten
- Fahrzeuge empfehlen
- eine Rückfrage stellen

Kontext:
{extra}

Fahrzeuge:
{car_text}

Kunde: {prompt}
""")

                answer = response.text

            except Exception:
                answer = "⏳ Bitte später erneut versuchen."

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# =========================
# 📞 LEAD FORMULAR
# =========================

st.divider()
st.subheader("📞 Persönliche Beratung anfragen")

with st.form("lead_form"):

    name = st.text_input("Name")
    phone = st.text_input("Telefonnummer")
    email = st.text_input("E-Mail")

    car_interest = st.selectbox(
        "Wunschfahrzeug",
        ["Audi A3", "Audi A4", "Audi A6", "Audi Q3", "Audi Q5", "Audi Q7"]
    )

    budget = st.selectbox(
        "Budget",
        ["Unter 30.000€", "30.000€ - 50.000€", "Über 50.000€"]
    )

    message = st.text_area("Nachricht")

    submitted = st.form_submit_button("🚀 Anfrage senden")

    if submitted:
        if not name or not phone:
            st.error("❌ Bitte Name und Telefonnummer eingeben")
        else:
            lead = {
                "name": name,
                "phone": phone,
                "email": email,
                "car": car_interest,
                "budget": budget,
                "message": message
            }

            st.session_state.leads.append(lead)

            st.success("✅ Anfrage gesendet! Wir melden uns zeitnah.")

# =========================
# 📊 DASHBOARD
# =========================

st.sidebar.title("📊 Dashboard")
st.sidebar.write(f"Leads: {len(st.session_state.leads)}")

if st.sidebar.button("Leads anzeigen"):
    for lead in st.session_state.leads:
        st.sidebar.write(lead)