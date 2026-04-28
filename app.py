import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration de la page
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿", layout="centered")

# 2. Design : Masquer les menus Streamlit pour faire "Application Pro"
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Titre et Introduction
st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez les problèmes de vos plantes et découvrez les solutions naturelles Jungle Feed.")

# 4. Configuration de l'IA (Mode Sans Frais / France)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API introuvable dans les Secrets de Streamlit.")
    st.stop()

# 5. Catalogue exclusif Jungle Feed
CATALOGUE = """
UTILISE UNIQUEMENT CES SOLUTIONS JUNGLE FEED :
- Thrips / Moucherons / Cochenilles : 'Kit Anti-Thrips Ultime' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles uniquement : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Araignées Rouges : 'Kit Spécial Araignée Rouge' (https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens)
- Moucherons de terreau : 'Kit Anti-Moucherons 3-en-1' (https://www.junglefeed.fr/products/kit-anti-moucherons-3-en-1-naturel)
- Nutrition : 'Engrais Plantes d'Intérieur Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Soin préventif : 'Huile de Neem Prête à l'emploi' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
- Enracinement : 'Eau de Saule Pure' (https://www.junglefeed.fr/products/eau-de-saule-pure-naturelle)
"""

# 6. Interface de capture
img_file = st.camera_input("Scanner une feuille malade")
if not img_file:
    img_file = st.file_uploader("OU charger une photo", type=['jpg', 'png', 'jpeg'])

# 7. Analyse et Diagnostic
if img_file is not None:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)

    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("L'expert Jungle Feed analyse votre plante..."):
            try:
                # Détection automatique du modèle disponible
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                selected_model = next((m for m in available_models if 'flash' in m), available_models[0])

                model = genai.GenerativeModel(selected_model)
                
                prompt = f"""Tu es l'agronome expert de la marque Jungle Feed.
                Analyse cette photo pour identifier la maladie ou le parasite.
                
                RÉPONDS SELON CE PLAN :
                1. Diagnostic précis.
                2. Cause (une phrase).
                3. Recommande
