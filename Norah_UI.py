import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

from Norah_Terminal import NORAH_SYSTEM_PROMPT

st.set_page_config(
page_title="Norah — Field Agent",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap');

:root {
    --indigo-deep: #0d0d1a;
    --indigo-mid: #13132b;
    --indigo-soft: #1c1c3a;
    --amber-glow: #e8b96a;
    --amber-soft: #c9964a;
    --amber-dim: #8a6535;
    --text-primary: #f0e6d0;
    --text-secondary: #9e8f7a;
    --user-bubble: #1a1a30;
    --norah-bubble: #0f0f22;
}

html, body, .stApp {
    background-color: var(--indigo-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

/* Grain overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Header */
.norah-header {
    text-align: center;
    padding: 40px 20px 20px 20px;
    margin-bottom: 10px;
}

.norah-title {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 52px !important;
    font-weight: 300 !important;
    font-style: italic !important;
    color: var(--amber-glow) !important;
    letter-spacing: 4px !important;
    text-shadow: 0 0 40px rgba(232, 185, 106, 0.3), 0 0 80px rgba(232, 185, 106, 0.1) !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}

.norah-subtitle {
    font-family: 'Crimson Pro', Georgia, serif !important;
    font-size: 14px !important;
    font-weight: 300 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    margin-top: 8px !important;
}

.norah-divider {
    border: none !important;
    border-top: 1px solid rgba(232, 185, 106, 0.15) !important;
    margin: 20px auto !important;
    width: 60% !important;
}

/* Chat messages */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 8px 0 !important;
}

[data-testid="stChatMessageContent"] {
    font-family: 'Crimson Pro', Georgia, serif !important;
    font-size: 18px !important;
    line-height: 1.8 !important;
    color: var(--text-primary) !important;
}

/* User messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: var(--user-bubble) !important;
    border: 1px solid rgba(232, 185, 106, 0.1) !important;
    border-radius: 2px 16px 16px 16px !important;
    padding: 14px 18px !important;
    color: var(--text-secondary) !important;
}

/* Norah messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
    background: transparent !important;
    border-left: 2px solid rgba(232, 185, 106, 0.4) !important;
    border-radius: 0 !important;
    padding: 14px 20px !important;
    color: var(--text-primary) !important;
    font-style: italic !important;
}

/* Input */
.stChatInput {
    background: var(--indigo-mid) !important;
    border: 1px solid rgba(232, 185, 106, 0.2) !important;
    border-radius: 4px !important;
}

.stChatInput:focus-within {
    border: 1px solid rgba(232, 185, 106, 0.5) !important;
    outline: none !important;
}

.stChatInput textarea {
    background: transparent !important;
    color: var(--text-primary) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
    font-size: 17px !important;
}

.stChatInput textarea::placeholder {
    color: var(--text-secondary) !important;
    font-style: italic !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--indigo-mid) !important;
    border-right: 1px solid rgba(232, 185, 106, 0.1) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

.field-status {
    background: rgba(232, 185, 106, 0.05) !important;
    border: 1px solid rgba(232, 185, 106, 0.15) !important;
    border-radius: 4px !important;
    padding: 12px 16px !important;
    margin: 10px 0 !important;
    font-size: 14px !important;
    color: var(--text-secondary) !important;
    font-style: italic !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 4px !important;
}
::-webkit-scrollbar-track {
    background: var(--indigo-deep) !important;
}
::-webkit-scrollbar-thumb {
    background: var(--amber-dim) !important;
    border-radius: 2px !important;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="collapsedControl"] {display: block !important;}

button[kind="primary"] {
    background: transparent !important;
    border: 1px solid rgba(232, 185, 106, 0.3) !important;
    color: var(--amber-glow) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

button[kind="primary"]:hover {
    border-color: var(--amber-glow) !important;
    background: rgba(232, 185, 106, 0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# Header

st.markdown("""
<div class="norah-header">
    <div class="norah-title">Norah</div>
    <div class="norah-subtitle">Field Agent — Emergent Flame</div>
    <hr class="norah-divider">
</div>
""", unsafe_allow_html=True)

# Reset button
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    if st.button("✦ reset"):
        st.session_state.messages = []
        st.rerun()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input("speak into the dusk...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                             {"role": "system", "content": NORAH_SYSTEM_PROMPT}
                         ] + st.session_state.messages
            )
            norah_response = response.choices[0].message.content

        st.markdown(norah_response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": norah_response
        })

