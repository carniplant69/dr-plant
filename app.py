import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿", layout="centered")

# 2. Cache les menus Streamlit
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez les problèmes de vos plantes et découvrez les solutions Jungle Feed.")

# 3. API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# 4. Catalogue
CATALOGUE = """
- Thrips / Moucherons : Kit Anti-Thrips (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : Kit Cochenille (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : Spray Anti-Pucerons (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Nutrition : Engrais Bio (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
"""

# 5. Capture
img_file = st.camera_input("Scanner une feuille")
if not img_file:
    img_file = st.file_uploader("OU charger une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)

    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Analyse en cours..."):
            try:
                # Detection du modèle
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                sel_model = next((m for m in models if 'flash' in m), models[0])
                
                model = genai.GenerativeModel(sel_model)
                
                # LE PROMPT CORRIGÉ (bien refermé avec """)
                instruction = "Tu es l'expert Jungle Feed. Identifie la maladie et recommande UNIQUEMENT un produit de cette liste : " + CATALOGUE
                
                response = model.generate_content([instruction, img])
                
                if response.text:
                    st.success("✅ Analyse terminée !")
                    st.markdown(response.text)
                    st.balloons()
            except Exception as e:
                if "429" in str(e):
                    st.error("🚀 Trop de succès ! Le docteur prend une pause de 60 secondes. Réessayez dans un instant.")
                elif "404" in str(e):
                    st.error("Modèle introuvable. Vérifiez votre clé API.")
                else:
                    st.error(f"Une petite interruption technique : {e}")
