import streamlit as st
import wikipediaapi
import google.generativeai as genai

#  API
GENAI_KEY = st.secrets.get("GENAI_KEY", None)

if not GENAI_KEY:
    st.error("Falta la API KEY en secrets")
    st.stop()

genai.configure(api_key=GENAI_KEY)
genai.GenerativeModel('gemini-1.5-pro')

#  ESTILO PERSONALIZADO (ROSADO NEÓN + NEGRO)
st.markdown("""
    <style>
    body {
        background-color: #0a0a0a;
        color: white;
    }
    .stApp {
        background-color: #0a0a0a;
    }
    h1 {
        color: #ff4df0;
        text-align: center;
        text-shadow: 0 0 10px #ff4df0;
    }
    .chat-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px #ff4df0;
    }
    </style>
""", unsafe_allow_html=True)

# Wikipedia
wiki = wikipediaapi.Wikipedia(
    language='es',
    user_agent="FenputadoraBot/1.0"
)

def obtener_contexto_wiki(tema):
    try:
        page = wiki.page(tema)
        if page.exists():
            return page.summary[:600]
    except:
        return ""
    return ""

#  MEMORIA DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

#  TÍTULO
st.markdown("<h1> Fenputadora AI </h1>", unsafe_allow_html=True)
st.write("Tu asistente en Sistemas Digitales y Tecnología ")

#  INPUT
user_message = st.text_input(" Escribe tu pregunta (Ej: ¿Qué es un sistema digital?)")

if user_message:
    temas_tecnicos = ["arduino", "compuerta", "sistema digital", "onda", "circuito", "tecnologia"]
    contexto = ""

    for tema in temas_tecnicos:
        if tema in user_message.lower():
            contexto = obtener_contexto_wiki(tema)
            break

    prompt = f"""
Eres 'Fenputadora', una profesora experta en Sistemas Digitales y Tecnología.

MODO PROFESINAL :

 forma de responder:
- Explicas como docente universitario
- Das definiciones claras
- Incluyes ejemplos prácticos
- Si aplica, muestras tablas de verdad
- Explicas paso a paso
- Usas analogías fáciles

IMPORTANTE:
- Responde SOLO temas de tecnología y sistemas digitales
- Si el tema es lógico (AND, OR, NOT), incluye tabla de verdad

Contexto técnico: {contexto}

Pregunta del estudiante: {user_message}

Respuesta:
"""
try:
    response = model.generate_content(prompt)

    if response.candidates:
        reply = response.candidates[0].content.parts[0].text
    else:
        reply = "No pude generar respuesta, intenta otra vez"

except Exception as e:
    reply = f"Error: {e}"
    # Guardar conversación
    st.session_state.messages.append(("Tú", user_message))
    st.session_state.messages.append(("Fenputadora", reply))

#  MOSTRAR CHAT
for sender, msg in st.session_state.messages:
    st.markdown(f"""
    <div class="chat-box">
        <b>{sender}:</b><br>{msg}
    </div>
    """, unsafe_allow_html=True)
