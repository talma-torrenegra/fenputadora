import streamlit as st
import wikipediaapi
from google import genai

# 1. CONFIGURACIÓN DE API Y MODELO
GENAI_KEY = st.secrets.get("GENAI_KEY", None)

if not GENAI_KEY:
    st.error("Falta la API KEY en secrets")
    st.stop()

client = genai.Client(api_key=GENAI_KEY)

# 2. ESTILO PERSONALIZADO (ROSADO NEÓN + NEGRO)
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
    }
    h1 {
        color: #ff4df0;
        text-align: center;
        text-shadow: 0 0 10px #ff4df0;
        font-family: 'Courier New', Courier, monospace;
    }
    .chat-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #ff4df0;
        box-shadow: 0 0 8px #ff4df0;
        color: white;
    }
    .user-label { color: #00f2ff; font-weight: bold; }
    .bot-label { color: #ff4df0; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. CONFIGURACIÓN DE WIKIPEDIA
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

# 4. MEMORIA DE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. INTERFAZ DE USUARIO
st.markdown("<h1> Fenputadora AI </h1>", unsafe_allow_html=True)
st.write("Tu asistente en Sistemas Digitales y Tecnología")

with st.form(key='chat_form', clear_on_submit=True):
    user_message = st.text_input("Escribe tu pregunta (Ej: ¿Qué es una compuerta AND?)")
    submit_button = st.form_submit_button(label='Enviar')

# 6. LÓGICA DE RESPUESTA
if submit_button and user_message:

    temas_tecnicos = ["arduino", "compuerta", "sistema digital", "onda", "circuito", "tecnologia", "binario"]
    contexto = ""

    for tema in temas_tecnicos:
        if tema in user_message.lower():
            contexto = obtener_contexto_wiki(tema)
            break

    prompt = f"""
    Eres 'Fenputadora', una profesora experta en Sistemas Digitales y Tecnología.

    MODO PROFESIONAL:
    - Explicas como docente universitario.
    - Das definiciones claras y verídicas.
    - Incluyes ejemplos prácticos.
    - Si el tema es sobre compuertas lógicas, incluye tabla de verdad.

    Contexto extra: {contexto}
    Pregunta del estudiante: {user_message}
    Respuesta:
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        reply = response.text

    except Exception as e:
        reply = f"Error de conexión: {str(e)}"

    st.session_state.messages.append(("Tú", user_message))
    st.session_state.messages.append(("Fenputadora", reply))

# 7. VISUALIZACIÓN DEL CHAT
chat_placeholder = st.container()

with chat_placeholder:
    for sender, msg in st.session_state.messages:
        label_class = "user-label" if sender == "Tú" else "bot-label"
        st.markdown(f"""
            <div class="chat-box">
                <span class="{label_class}">{sender}:</span><br>
                {msg}
            </div>
        """, unsafe_allow_html=True)
