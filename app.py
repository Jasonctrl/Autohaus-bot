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

.stApp {
    background-color: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #222;
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
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ef233c;
    transform: scale(1.02);
}

[data-testid="stChatMessage"] {
    background-color: #1f2937;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

.stChatInput input {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 10px !important;
}

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
# 🖼️ AUDI BILDER GALERIE
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "https://source.unsplash.com/800x600/?audi,sportscar",
        caption="Audi Sport",
        use_container_width=True
    )

with col2:
    st.image(
        "https://source.unsplash.com/800x600/?luxury,car",
        caption="Premium Fahrzeuge",
        use_container_width=True
    )

with col3:
    st.image(
        "https://source.unsplash.com/800x600/?electric,car",
        caption="E-Mobilität",
        use_container_width=True
    )

# ==================================================
# 💬 CHAT VERLAUF
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

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
                response = model.generate_content(f"""
Du bist ein professioneller Audi Verkaufsberater.

Regeln:
- freundlich
- modern
- verkaufsorientiert
- empfehle Audi Modelle
- stelle Rückfragen

Kunde:
{prompt}
""")

                answer = response.text

            except Exception:
                answer = "⏳ Fehler oder zu viele Anfragen. Bitte erneut versuchen."

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })