import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Look & Feel Jungle Feed
st.set_page_config(page_title="Dr. Plant Jungle Feed", page_icon="🌿")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stButton>button {background-color: #2D5A27; color: white; border-radius: 20px; width: 100%; font-weight: bold;}</style>", unsafe_allow_html=True)

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez vos parasites et trouvez la solution Jungle Feed adaptée.")

# 2. Config API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Configurez la clé API dans les Secrets.")
    st.stop()

# 3. Catalogue
CATALOGUE = """
- Thrips / Moucherons / Cochenilles : 'Kit Anti-Thrips Ultime' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Nutrition : 'Engrais Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Soin : 'Huile de Neem' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
"""

# 4. Interface
img_file = st.camera_input("📸 Prenez une photo")
if not img_file:
    img_file = st.file_uploader("OU choisissez une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer l'analyse Jungle Feed 🚀"):
        with st.spinner("L'expert analyse..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "Tu es l'agronome expert Jungle Feed. Identifie la maladie sur cette photo. Recommande UN produit de cette liste avec son lien : " + CATALOGUE
                response = model.generate_content([prompt, img])
                st.success("✅ Diagnostic terminé !")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Erreur : {e}")
