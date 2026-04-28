import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Diagnostic Jungle Feed")

# 2. Sécurité de la Clé API
if "GEMINI_API_KEY" in st.secrets:
    # On initialise avec la clé des Secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ La clé GEMINI_API_KEY est manquante dans les Secrets de Streamlit.")
    st.stop()

# 3. Interface
img_file = st.camera_input("Prendre une photo de la feuille")
if not img_file:
    img_file = st.file_uploader("OU choisir une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Analyse en cours..."):
            try:
                # FORCE le nom du modèle sans le préfixe 'models/' si le 404 persiste
                # On teste la version la plus stable pour les comptes Pro
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """Tu es l'agronome expert de Jungle Feed. 
                Identifie la maladie sur cette photo.
                Propose uniquement un produit de la gamme Jungle Feed (ex: Huile de Neem, Purin d'Ortie, Kit Thrips).
                Donne le lien : https://www.junglefeed.fr/collections/soins"""

                # On génère le contenu
                response = model.generate_content([prompt, img])
                
                st.success("Analyse réussie !")
                st.markdown(response.text)

            except Exception as e:
                # Si le premier essai échoue, on tente avec le nom complet
                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content([prompt, img])
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Erreur persistante : {e2}")
                    st.info("Vérifie dans Google AI Studio que ta clé est bien 'Pay-as-you-go' et que l'API Gemini est activée.")
