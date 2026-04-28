import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Diagnostic Expert")

# 2. Récupération PROPRE de la clé
# On ne touche plus à cette partie, tout se passe dans les réglages Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# 3. Interface
img_file = st.camera_input("Scanner une feuille")
if not img_file:
    img_file = st.file_uploader("Ou envoyer une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Analyse..."):
            try:
                # On utilise le nom universel
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(["Identifie la maladie et donne une solution Jungle Feed.", img])
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Détail de l'erreur : {e}")
