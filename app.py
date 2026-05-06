import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config de la page & Design Pro
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿", layout="centered")

# CSS pour un look "App Mobile" sans les menus Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        background-color: #2D5A27;
        color: white;
        border-radius: 15px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez vos parasites et trouvez la solution Jungle Feed adaptée.")

# 2. Initialisation API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API manquante dans les Secrets.")
    st.stop()

# 3. Catalogue de soins
CATALOGUE = """
UTILISE UNIQUEMENT CES SOLUTIONS JUNGLE FEED :
- Thrips / Moucherons / Cochenilles : 'Kit Anti-Thrips Ultime' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Nutrition : 'Engrais Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Protection : 'Huile de Neem Prête à l'emploi' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
"""

# 4. Scanner
img_file = st.camera_input("📸 Prenez une photo de la feuille")
if not img_file:
    img_file = st.file_uploader("OU choisissez une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer l'analyse Jungle Feed 🚀"):
        with st.spinner("L'expert analyse votre plante..."):
            try:
                # Sélection auto du modèle
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Tu es l'expert agronome Jungle Feed. Diagnostic précis de la maladie sur cette photo. Recommande UN produit de cette liste avec son lien : {CATALOGUE}. Sois bref et pro."
                
                response = model.generate_content([prompt, img])
                
                st.success("✅ Diagnostic terminé !")
                st.markdown(response.text)
                st.balloons()

            except Exception as e:
                if "429" in str(e):
                    st.warning("⏳ Trop de succès ! Le docteur fait une pause. Réessayez dans 1 minute.")
                else:
                    st.error(f"Oups, une petite erreur : {e}")
