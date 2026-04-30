import streamlit as st
import wikipediaapi
import google.generativeai as genai



app = Flask(__name__)

# === CONFIGURACIÓN ===
# Consigue tu clave en https://aistudio.google.com/
GENAI_KEY = "AIzaSyAk1ztkcPQ6tgqkdt8CScC5dRgofUqWvyw" 
genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Versión rápida y fluida

# Configuración de Wikipedia con User-Agent para evitar bloqueos
wiki = wikipediaapi.Wikipedia(
    language='es',
    user_agent="FenputadoraBot/1.0 (jorge_estudiante_ingenieria)"
)

def obtener_contexto_wiki(tema):
    """Busca en Wikipedia para asegurar que Fenputadora no invente datos técnicos."""
    try:
        page = wiki.page(tema)
        if page.exists():
            return page.summary[:600]
    except:
        return ""
    return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    
    # Palabras clave para reforzar la búsqueda técnica
    temas_tecnicos = ["arduino", "compuerta", "sistema digital", "onda cuadrada", "semaforo"]
    contexto = ""
    
    for tema in temas_tecnicos:
        if tema in user_message.lower():
            contexto = obtener_contexto_wiki(tema)
            break

    # Prompt para darle la personalidad fluida y seria
    prompt = f"""
    Eres 'Fenputadora', la asistente virtual avanzada de Sistemas Digitales.
    Tu objetivo es ayudar a estudiantes de Ingeniería de Sistemas.
    Personalidad: Fluida, seria, profesional y muy clara. Habla como un colega experto.
    
    Contexto técnico extraído de Wikipedia: {contexto}
    
    Pregunta del usuario: {user_message}
    
    Respuesta fluida:
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Error en el núcleo de datos. ¿Podrías repetir la consulta?"})

if __name__ == '__main__':
    # Usamos 0.0.0.0 para que sea accesible desde el celular escaneando el QR
    app.run(host='0.0.0.0', port=5000, debug=True)
