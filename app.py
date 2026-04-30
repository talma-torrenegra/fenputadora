import streamlit as st
import wikipediaapi
import google.generativeai as genai

#  API
GENAI_KEY = st.secrets.get("GENAI_KEY", None)

if not GENAI_KEY:
    st.error("Falta la API KEY en secrets")
    st.stop()

genai.configure(api_key=GENAI_KEY)
# Cambia esta línea para asegurar compatibilidad
model = genai.GenerativeModel('gemini-1.5-flash') 

# ... (todo tu código de estilo y Wikipedia igual) ...

# INPUT
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
    MODO PROFESIONAL:
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

    # MOVEMOS EL TRY ADENTRO DEL IF USER_MESSAGE
    try:
        response = model.generate_content(prompt)
        
        if response.candidates:
            reply = response.text # Forma más directa de obtener el texto
        else:
            reply = "No pude generar respuesta, intenta otra vez"

    except Exception as e:
        reply = f"Error: {e}"
    
    # Guardar conversación (dentro del IF para que solo guarde si hubo mensaje)
    st.session_state.messages.append(("Tú", user_message))
    st.session_state.messages.append(("Fenputadora", reply))

# MOSTRAR CHAT
for sender, msg in st.session_state.messages:
    st.markdown(f"""
    <div class="chat-box">
        <b>{sender}:</b><br>{msg}
    </div>
    """, unsafe_allow_html=True)
    """, unsafe_allow_html=True)
