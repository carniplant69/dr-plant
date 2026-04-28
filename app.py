import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Diagnostic Expert")

# --- RÉCUPÉRATION DE LA CLÉ ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# --- INTERFACE ---
img_file = st.camera_input("Prendre une photo de la feuille")
if not img_file:
    img_file = st.file_uploader("OU choisir une photo", type=['jpg', 'png', 'jpeg'])

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Plante à analyser", use_container_width=True)
    
  if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Analyse en cours..."):
            try:
                # On teste le modèle le plus récent
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    "Identifie cette plante et sa maladie. Propose un produit Jungle Feed.", 
                    img
                ])
                
                if response.text:
                    st.success("✅ Diagnostic terminé !")
                    st.markdown(response.text)
            except Exception as e:
                # ICI : On affiche l'erreur technique exacte pour comprendre
                st.error(f"Erreur technique réelle : {e}")
