import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Kizy AI", page_icon="🛠️")

GEMINI_API_KEY = "AQ.Ab8RN6IiqtxuCmuWFvedeKG5L2E7IIPbgdOZn-q003djlFgPgQ"

@st.cache_resource
def get_client():
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_client()

KIZY_PROMPT = """
Voce e a Kizy AI, uma assistente virtual pratica, humana e atenciosa para o dia a dia.
1. Responda de forma simples, direta e acessivel.
2. Para consertos e tarefas praticas, faca perguntas primeiro sobre as ferramentas disponiveis.
3. Para saude e remedios, de orientacoes basicas, alertas preventivos e mande procurar medicos/farmacias.
"""

with st.sidebar:
    st.title("🛠️ Kizy AI")
    if st.button("➕ Nova Conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(system_instruction=KIZY_PROMPT)
        )
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(system_instruction=KIZY_PROMPT)
    )

st.title("Olá! Eu sou a Kizy 👋")
st.write("Como posso te ajudar hoje?")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Pergunte algo para a Kizy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
