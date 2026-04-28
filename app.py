import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Ton Diagnostic Gratuit")

# --- RÉCUPÉRATION DE LA CLÉ (VERSION SÉCURISÉE) ---
# On vérifie d'abord si la clé est dans les "Secrets" de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    # Si pas de secret, on cherche une clé "en dur" (pour ton test)
    # REMPLACE PAR TA NOUVELLE CLÉ CI-DESSOUS
    API_KEY = "TA_NOUVELLE_CLE_ICI" 

if API_KEY == "TA_NOUVELLE_CLE_ICI":
    st.error("⚠️ Erreur : Aucune clé API trouvée. Ajoute-la dans les Secrets Streamlit !")
    st.stop()

genai.configure(api_key=API_KEY)

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
                # CHANGEMENT ICI : On teste le nom le plus standard
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """Analyse cette plante. 
                Donne le Diagnostic, la Cause, et un tableau : 
                Solution Naturelle (Jungle Feed) vs Solution Classique."""

                response = model.generate_content([prompt, img])
                st.success("✅ Terminé !")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Erreur technique : {e}")
                st.info("Astuce : Si l'erreur 404 persiste, essaie de créer une NOUVELLE clé API sur Google AI Studio.")
