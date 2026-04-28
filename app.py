import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Expert Jungle Feed")

# 2. Connexion intelligente
if "GEMINI_API_KEY" in st.secrets:
    # 'transport=rest' est obligatoire pour la stabilité en France (Free Tier)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Ajoute GEMINI_API_KEY dans les Secrets Streamlit.")
    st.stop()

# 3. Ton Catalogue Jungle Feed
CATALOGUE = """
- Thrips / Moucherons : 'Kit Anti-Thrips' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Spray Anti-Pucerons' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Nutrition : 'Engrais Bio' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
"""

# 4. Interface
img_file = st.camera_input("Scanner une feuille")
if not img_file:
    img_file = st.file_uploader("Ou charger une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Recherche du meilleur modèle disponible sur ton compte..."):
            try:
                # ÉTAPE MAGIQUE : On liste les modèles autorisés pour TA clé
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # On cherche en priorité un modèle 'flash'
                selected_model = None
                for m in available_models:
                    if 'flash' in m:
                        selected_model = m
                        break
                
                # Si pas de flash, on prend le premier qui gère le contenu (souvent gemini-pro)
                if not selected_model:
                    selected_model = available_models[0]

                # Lancement de l'analyse avec le modèle trouvé
                model = genai.GenerativeModel(selected_model)
                prompt = f"Tu es l'expert Jungle Feed. Identifie la maladie et recommande UNIQUEMENT un produit de cette liste : {CATALOGUE}. Donne le lien."
                
                response = model.generate_content([prompt, img])
                
                st.success("✅ Analyse terminée !")
                st.markdown(response.text)
                st.balloons()

            except Exception as e:
                st.error(f"Désolé, ton compte Google bloque encore l'accès : {e}")
                st.info("💡 ACTION REQUISE : Va sur Google AI Studio, supprime TOUTES tes clés et recrée-en une SEULE. C'est souvent la seule façon de réinitialiser les droits en plan gratuit.")
