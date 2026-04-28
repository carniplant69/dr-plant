import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Ton Diagnostic Gratuit")

# --- CONFIGURATION API ---
# On va chercher la clé dans les réglages cachés de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ Clé API non configurée dans les Secrets de Streamlit.")
    st.stop() # On arrête l'appli ici si pas de clé

# --- CAPTURE IMAGE ---
img_file = st.camera_input("Prendre une photo de la feuille malade")

if not img_file:
    img_file = st.file_uploader("OU choisis une photo", type=['jpg', 'png', 'jpeg'])

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Analyse en cours...", use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("L'expert Jungle Feed analyse ta plante..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = """Tu es l'expert agronome de Jungle Feed. 
                Analyse cette plante : Diagnostic, Cause, et Tableau (Solution Naturelle Jungle Feed vs Solution Classique)."""

                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("✅ Diagnostic terminé !")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Erreur : {e}")
