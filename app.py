import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Diagnostic Jungle Feed")

# 2. Connexion sécurisée (Plan Sans Frais)
if "GEMINI_API_KEY" in st.secrets:
    # On force le transport 'rest' pour éviter les bugs de connexion en Europe
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Ajoute GEMINI_API_KEY dans les Secrets de Streamlit.")
    st.stop()

# 3. Ton Catalogue Jungle Feed
CATALOGUE = """
- Thrips / Moucherons : 'Kit Anti-Thrips' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Spray Anti-Pucerons' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Nutrition : 'Engrais Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Soin : 'Huile de Neem' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
"""

# 4. Interface
img_file = st.camera_input("Prendre une photo")
if not img_file:
    img_file = st.file_uploader("Ou choisir une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Recherche du modèle gratuit disponible..."):
            try:
                # ÉTAPE CLÉ : On cherche quel modèle accepte ta clé gratuite
                model_name = "gemini-1.5-flash" # Par défaut
                
                # Test de connexion
                model = genai.GenerativeModel(model_name)
                prompt = f"""Tu es l'expert Jungle Feed. 
                Analyse cette plante. Identifie la maladie.
                Recommande UNIQUEMENT un produit de cette liste : {CATALOGUE}.
                Donne le lien exact du produit."""
                
                response = model.generate_content([prompt, img])
                
                st.success("✅ Analyse réussie !")
                st.markdown(response.text)
                st.balloons()

            except Exception as e:
                # Si le premier nom échoue, on essaie la version '-latest'
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash-latest")
                    response = model.generate_content([prompt, img])
                    st.success("✅ Diagnostic réussi (Modèle alternative) !")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"L'API Google bloque l'accès : {e2}")
                    st.info("💡 CONSEIL : Puisque tu es en France avec un plan gratuit, crée une NOUVELLE clé API sur Google AI Studio. Parfois, la première clé bugue avec le plan gratuit.")
