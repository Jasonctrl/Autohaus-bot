import streamlit as st
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# ==================================================
# 🚗 AUDI KI VERKAUFSASSISTENT
# ==================================================

st.set_page_config(
    page_title="Audi Verkaufsassistent",
    page_icon="🚗",
    layout="wide"
)

# ==================================================
# 🎨 AUDI PREMIUM DESIGN
# ==================================================

st.markdown("""
<style>

/* Hintergrund */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #222;
}

/* Überschriften */
h1, h2, h3 {
    color: white;
}

/* Buttons */
.stButton>button {
    background-color: #d90429;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ef233c;
    transform: scale(1.02);
}

/* Chat Nachrichten */
[data-testid="stChatMessage"] {
    background-color: #1f2937;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

/* Chat Input */
.stChatInput input {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Info Box */
[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# 🔐 API KEY LADEN
# ==================================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Kein API Key gefunden!")
    st.stop()

# ==================================================
# 🤖 GEMINI KONFIGURATION
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
✔ Premium Fahrzeug-Empfehlungen  
✔ Lead-Generierung  
✔ Verkaufsunterstützung  
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
# 🚗 PREMIUM AUTO BILD
# ==================================================

st.image(
    "https://images.unsplash.com/photo-1503376780353-7e6692767b70",
    use_container_width=True
)

# ==================================================
# 🚘 FAHRZEUGKARTEN
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
    st.button("Probefahrt RS6")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1767749995462-9fe0890d5960?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        use_container_width=True
    )
    st.markdown("### Audi Q8")
    st.write("💰 Ab 89.000 €")
    st.write("✔ Luxus SUV")
    st.write("✔ Hybrid Technologie")
    st.button("Probefahrt Q8")

with col3:
    st.image(
        "https://images.unsplash.com/photo-1502877338535-766e1452684a",
        use_container_width=True
    )
    st.markdown("### Audi A5")
    st.write("💰 Ab 58.000 €")
    st.write("✔ Sportlich")
    st.write("✔ Premium Komfort")
    st.button("Probefahrt A5")

# ==================================================
# 💬 CHAT VERLAUF
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================================================
# ⏳ ANTI SPAM
# ==================================================

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ==================================================
# 💬 CHAT INPUT
# ==================================================

prompt = st.chat_input("Wie kann ich Ihnen helfen?")

if prompt:

    current_time = time.time()

    # Spam Schutz
    if current_time - st.session_state.last_time < 5:
        st.warning("⏳ Bitte kurz warten...")
        st.stop()

    st.session_state.last_time = current_time

    # User Nachricht speichern
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ==================================================
    # 🤖 KI ANTWORT
    # ==================================================

    with st.chat_message("assistant"):

        with st.spinner("🚗 Audi KI denkt nach..."):

            try:

                response = model.generate_content(
                    f"""
Du bist ein professioneller Audi Verkaufsberater.

Dein Ziel:
- Kunden beraten
- Premium Fahrzeuge empfehlen
- Leads generieren
- professionell verkaufen

Regeln:
- freundlich
- modern
- verkaufsorientiert
- stelle Rückfragen
- empfehle passende Audi Modelle
- antworte professionell

Kunde:
{prompt}
"""
                )

                answer = response.text

            except Exception:
                answer = "⏳ Zu viele Anfragen. Bitte kurz warten und erneut versuchen."

        st.markdown(answer)

    # Antwort speichern
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

    name = st.text_input("Name")
    email = st.text_input("E-Mail")
    telefon = st.text_input("Telefon")
    interesse = st.selectbox(
        "Interessiertes Modell",
        ["Audi RS6", "Audi Q8", "Audi A5"]
    )

    senden = st.form_submit_button("Anfrage senden")

    if senden:
        st.success("✅ Anfrage erfolgreich gesendet!")
        st.write(f"Vielen Dank {name}, wir melden uns schnellstmöglich.")