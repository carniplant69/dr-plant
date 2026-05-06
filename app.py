import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION VISUELLE & MARQUE ---
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿", layout="centered")

# CSS pour cacher les menus Streamlit et personnaliser le bouton
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        background-color: #2D5A27;
        color: white;
        border-radius: 20px;
        width: 100%;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("L'intelligence artificielle au service de vos plantes d'intérieur.")

# --- 2. CONNEXION API ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# --- 3. CATALOGUE PRODUITS JUNGLE FEED ---
# On centralise ici pour pouvoir le modifier facilement
CATALOGUE = """
- Thrips / Moucherons : 'Kit Anti-Thrips Ultime' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Araignées Rouges : 'Kit Spécial Araignée Rouge' (https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens)
- Nutrition : 'Engrais Plantes d'Intérieur Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Soin préventif : 'Huile de Neem Prête à l'emploi' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
"""

# --- 4. INTERFACE UTILISATEUR ---
img_file = st.camera_input("📸 Scannez votre plante")
if not img_file:
    img_file = st.file_uploader("OU chargez une photo de votre galerie", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic Jungle Feed 🚀"):
        with st.spinner("Analyse des feuilles en cours..."):
            try:
                # Sélection automatique du meilleur modèle
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                sel_model = next((m for m in models if 'flash' in m), models[0])
                model = genai.GenerativeModel(sel_model)
                
                # Prompt Expert
                prompt = f"Tu es l'expert agronome Jungle Feed. Identifie précisément la maladie sur cette photo. Propose uniquement un produit adapté de cette liste : {CATALOGUE}. Sois court, pro et rassurant."
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("✅ Diagnostic terminé !")
                    st.markdown(response.text)
                    st.balloons()

            except Exception as e:
                # Gestion intelligente des erreurs
                if "429" in str(e):
                    st.warning("⏳ Trop de demandes ! Le docteur fait une petite pause. Réessayez dans 60 secondes.")
                elif "404" in str(e):
                    st.error("Désolé, le service de diagnostic est momentanément indisponible (Erreur 404).")
                else:
                    st.error(f"Une petite erreur s'est glissée : {e}")

# --- 5. FOOTER ---
st.divider()
st.caption("Besoin d'aide supplémentaire ? Contactez-nous sur junglefeed.fr")
