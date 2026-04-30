import streamlit as st
from google import genai
import wikipediaapi

# API KEY
GENAI_KEY = st.secrets["GENAI_KEY"]
client = genai.Client(api_key=GENAI_KEY)

# Wikipedia
wiki = wikipediaapi.Wikipedia(language='es', user_agent="FenputadoraBot/1.0")

def obtener_contexto_wiki(tema):
    page = wiki.page(tema)
    return page.summary[:500] if page.exists() else ""

# UI
st.title("Fenputadora AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_message = st.text_input("Escribe tu pregunta")

if user_message:

    contexto = obtener_contexto_wiki(user_message)

    prompt = f"""
Eres una profesora de sistemas digitales.

Contexto: {contexto}
Pregunta: {user_message}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash-001",
        contents=prompt
    )

    reply = response.text

    st.session_state.messages.append(("Tú", user_message))
    st.session_state.messages.append(("Bot", reply))

for role, msg in st.session_state.messages:
    st.write(f"{role}: {msg}")
