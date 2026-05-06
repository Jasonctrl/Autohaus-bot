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

/* Gesamter Hintergrund */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #222;
}

/* Titel */
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

/* Eingabefeld */
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
# 💬 CHAT VERLAUF
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Nachrichten anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================================================
# ⏳ ANTI SPAM SCHUTZ
# ==================================================

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ==================================================
# 💬 USER INPUT
# ==================================================

prompt = st.chat_input("Wie kann ich Ihnen helfen?")

if prompt:

    current_time = time.time()

    # Verhindert Spam-Anfragen
    if current_time - st.session_state.last_time < 5:
        st.warning("⏳ Bitte kurz warten...")
        st.stop()

    st.session_state.last_time = current_time

    # User speichern
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
- Fahrzeuge empfehlen
- Premium Service bieten
- verkaufsorientiert antworten

Regeln:
- freundlich
- modern
- professionell
- stelle Rückfragen
- empfehle passende Audi Modelle
- antworte klar und hilfreich

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