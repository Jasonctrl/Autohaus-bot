import streamlit as st
import os
import time
import csv
import smtplib
import pandas as pd
import streamlit_authenticator as stauth

from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv

import google.generativeai as genai

# ==================================================
# 🚗 APP CONFIG
# ==================================================

st.set_page_config(
    page_title="Audi Verkaufsassistent",
    page_icon="🚗",
    layout="wide"
)

# ==================================================
# 🎨 DESIGN
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    background-color: #d90429;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #ef233c;
}

[data-testid="stChatMessage"] {
    background-color: #1f2937;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

.stTextInput input,
.stChatInput input {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# 🔐 LOGIN SYSTEM
# ==================================================

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "$2b$12$KIXQ0KXJ6t7lP6R7LQ5M6uT3J4bLQ7m6x3F8f9V5l9M4nB2d7H9aK"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "audi_dashboard",
    "abcdef",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login(
    location="main"
)

if authentication_status is False:
    st.error("❌ Benutzername oder Passwort falsch")
    st.stop()

if authentication_status is None:
    st.warning("🔐 Bitte anmelden")
    st.stop()

authenticator.logout("Logout", "sidebar")

st.sidebar.success(f"Willkommen {name}")

# ==================================================
# 🔐 API KEY
# ==================================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY fehlt")
    st.stop()

# ==================================================
# 🤖 GEMINI
# ==================================================

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# ==================================================
# 🚘 SIDEBAR
# ==================================================

st.sidebar.title("🚘 Audi Dashboard")

st.sidebar.info("""
Willkommen beim digitalen Audi Verkaufsassistenten.

✔ KI Beratung  
✔ Premium Fahrzeuge  
✔ Lead Generierung  
✔ CRM Dashboard  
✔ Login System  
""")

st.sidebar.success("✅ System Online")

# ==================================================
# 🚗 TITEL
# ==================================================

st.markdown("""
# 🚗 Audi KI Verkaufsassistent

### Premium Beratung für moderne Mobilität
""")

# ==================================================
# 🚗 HERO IMAGE
# ==================================================

st.image(
    "https://images.unsplash.com/photo-1503376780353-7e6692767b70",
    use_container_width=True
)

# ==================================================
# 🚘 FAHRZEUGE
# ==================================================

st.subheader("🔥 Beliebte Premium Modelle")

col1, col2, col3 = st.columns(3)

with col1:

    st.image(
        "https://images.unsplash.com/photo-1553440569-bcc63803a83d",
        use_container_width=True
    )

    st.markdown("### Audi RS6")
    st.write("💰 Ab 129.000 €")
    st.write("✔ 600 PS")
    st.write("✔ Quattro")

with col2:

    st.image(
        "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7",
        use_container_width=True
    )

    st.markdown("### Audi Q8")
    st.write("💰 Ab 89.000 €")
    st.write("✔ Luxus SUV")
    st.write("✔ Hybrid")

with col3:

    st.image(
        "https://images.unsplash.com/photo-1502877338535-766e1452684a",
        use_container_width=True
    )

    st.markdown("### Audi A5")
    st.write("💰 Ab 58.000 €")
    st.write("✔ Premium Komfort")

# ==================================================
# 💬 CHAT
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================================================
# ⏳ SPAM SCHUTZ
# ==================================================

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ==================================================
# 💬 INPUT
# ==================================================

prompt = st.chat_input("Wie kann ich Ihnen helfen?")

if prompt:

    current_time = time.time()

    if current_time - st.session_state.last_time < 5:
        st.warning("⏳ Bitte kurz warten...")
        st.stop()

    st.session_state.last_time = current_time

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🚗 Audi KI denkt nach..."):

            try:

                response = model.generate_content(
                    f"""
Du bist ein professioneller Audi Verkaufsberater.

Regeln:
- freundlich
- professionell
- verkaufsorientiert
- stelle Rückfragen
- empfehle passende Audi Modelle

Kunde:
{prompt}
"""
                )

                answer = response.text

            except Exception:
                answer = "⏳ Zu viele Anfragen. Bitte später erneut versuchen."

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ==================================================
# 📞 LEAD FORMULAR
# ==================================================

st.divider()

st.subheader("📞 Probefahrt oder Beratung anfragen")

with st.form("lead_form"):

    name_input = st.text_input("Name")
    email = st.text_input("E-Mail")
    telefon = st.text_input("Telefon")

    interesse = st.selectbox(
        "Interessiertes Modell",
        ["Audi RS6", "Audi Q8", "Audi A5"]
    )

    senden = st.form_submit_button("Anfrage senden")

    if senden:

        zeit = datetime.now().strftime("%d.%m.%Y %H:%M")

        daten = [
            zeit,
            name_input,
            email,
            telefon,
            interesse
        ]

        with open(
            "leads.csv",
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(daten)

        # ==================================================
        # 📧 EMAIL SENDEN
        # ==================================================

        try:

            absender = "Pjasondwayne@gmail.com"
            passwort = "bdrn hycs xmtm bita"

            empfaenger = "Pjasondwayne@gmail.com"

            nachricht = f"""
🚗 Neuer Lead

Name: {name_input}
E-Mail: {email}
Telefon: {telefon}
Fahrzeug: {interesse}

Zeit:
{zeit}
"""

            msg = MIMEText(nachricht)

            msg["Subject"] = "🚗 Neuer Autohaus Lead"
            msg["From"] = absender
            msg["To"] = empfaenger

            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                absender,
                passwort
            )

            server.send_message(msg)

            server.quit()

        except Exception:
            st.error("❌ E-Mail konnte nicht gesendet werden.")

        st.success("✅ Anfrage gespeichert!")

# ==================================================
# 📥 CSV DOWNLOAD
# ==================================================

st.divider()

st.subheader("📥 Lead Export")

if os.path.exists("leads.csv"):

    with open("leads.csv", "rb") as file:

        st.download_button(
            label="📥 Leads herunterladen",
            data=file,
            file_name="leads.csv",
            mime="text/csv"
        )

# ==================================================
# 📊 CRM DASHBOARD
# ==================================================

st.divider()

st.header("📊 CRM Dashboard")

if os.path.exists("leads.csv"):

    df = pd.read_csv(
        "leads.csv",
        header=None,
        names=[
            "Datum",
            "Name",
            "E-Mail",
            "Telefon",
            "Fahrzeug"
        ]
    )

    st.subheader("📈 Statistiken")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Gesamte Leads",
            len(df)
        )

    with col2:

        st.metric(
            "Beliebtestes Fahrzeug",
            df["Fahrzeug"].mode()[0]
        )

    st.subheader("🔍 Lead Suche")

    suche = st.text_input(
        "Nach Name oder Fahrzeug suchen"
    )

    if suche:

        gefiltert = df[
            df["Name"].str.contains(
                suche,
                case=False
            )
            |
            df["Fahrzeug"].str.contains(
                suche,
                case=False
            )
        ]

        st.dataframe(
            gefiltert,
            use_container_width=True
        )

    else:

        st.dataframe(
            df,
            use_container_width=True
        )

else:

    st.info("Noch keine Leads vorhanden.")