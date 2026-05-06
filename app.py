import streamlit as st
import os
import os
st.write("Images Ordner Inhalt:")
st.write(os.listdir("images"))
import time
from dotenv import load_dotenv
import google.generativeai as genai

# ==================================================
# 🚗 APP SETUP
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

</style>
""", unsafe_allow_html=True)

# ==================================================
# 🔐 API KEY
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
✔ KI Beratung  
✔ Premium Fahrzeuge  
✔ Verkaufsassistent  
""")

st.sidebar.success("Online")

# ==================================================
# 🚗 TITEL
# ==================================================

st.markdown("""
# 🚗 Audi KI Verkaufsassistent
### Premium Beratung für moderne Mobilität
""")
st.image("images/cadi.jpg")
# ==================================================
# 🖼️ AUTO BILDER (FIXE LINKS)
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70",
        caption="Sportliches Fahrzeug",
        use_container_width=True
    )

with col2:
    st.image(
        "https://images.unsplash.com/photo-1549924231-f129b911e442",
        caption="Premium Luxus Auto",
        use_container_width=True
    )

with col3:
    st.image(
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d",
        caption="Elektro & Zukunft",
        use_container_width=True
    )

# ==================================================
# 💬 CHAT SYSTEM
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ==================================================
# 💬 INPUT
# ==================================================

prompt = st.chat_input("Wie kann ich Ihnen helfen?")

if prompt:

    if time.time() - st.session_state.last_time < 5:
        st.warning("⏳ Bitte kurz warten...")
        st.stop()

    st.session_state.last_time = time.time()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚗 Audi KI denkt nach..."):

            try:
                response = model.generate_content(f"""
Du bist ein Audi Verkaufsberater.

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
                answer = "⏳ Fehler oder zu viele Anfragen."

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})