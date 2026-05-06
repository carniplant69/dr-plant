import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Dr. Plant Jungle Feed", page_icon="🌿")

# Design
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stButton>button {background-color: #2D5A27; color: white; border-radius: 20px; width: 100%;}</style>", unsafe_allow_html=True)

st.title("🌿 Dr. Plant : Diagnostic Expert")

# API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# Catalogue
CATALOGUE = "Solutions : Kit Anti-Thrips (https://www.junglefeed.fr/products/kit-ultime-anti-thrips), Kit Cochenille, Spray Pucerons, Engrais Bio."

img_file = st.camera_input("Prendre une photo")
if img_file:
    img = Image.open(img_file)
    st.image(img)
    if st.button("Lancer le diagnostic 🚀"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(["Identifie la maladie et propose un produit de cette liste : " + CATALOGUE, img])
            st.success("Analyse terminée !")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Erreur : {e}")
