import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Ton Diagnostic Gratuit")
st.write("Scanne ta plante, on te dit ce qu'elle a et comment la soigner !")

# --- CONFIGURATION API ---
# Remplace bien par TA clé API
API_KEY = "AIzaSyBv1lKm5F4zwhtgH34tJnGf1VGtay99L_E" 

if API_KEY == "AIzaSyBv1lKm5F4zwhtgH34tJnGf1VGtay99L_E":
    st.error("⚠️ Tu as oublié de mettre ta clé API Gemini dans le code !")
else:
    genai.configure(api_key=API_KEY)

# --- CAPTURE IMAGE ---
# On propose caméra ET envoi de fichier (plus fiable sur mobile)
img_file = st.camera_input("Prendre une photo de la feuille malade")

if not img_file:
    img_file = st.file_uploader("OU choisis une photo dans ta galerie", type=['jpg', 'png', 'jpeg'])

if img_file is not None:
    # Affichage de l'image
    img = Image.open(img_file)
    st.image(img, caption="Analyse en cours...", use_container_width=True)
    
    # Bouton pour lancer l'analyse (évite les appels API inutiles)
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("L'expert Jungle Feed analyse les cellules de ta plante..."):
            try:
                # Utilisation de Gemini 1.5 Flash (le plus rapide et efficace pour les images)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """Tu es l'expert agronome de Jungle Feed. 
                Analyse cette photo de plante. 
                1. Donne le diagnostic précis (maladie ou nuisible).
                2. Explique la cause en 1 phrase.
                3. Propose un tableau comparatif avec :
                   - Solution Naturelle (recommande un produit Jungle Feed adapté)
                   - Solution Classique (produit du commerce type Algoflash/Fertiligène)
                Sois pro, court et rassurant."""

                # On génère le contenu
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("✅ Diagnostic terminé !")
                    st.markdown(response.text)
                else:
                    st.warning("L'IA n'a pas pu identifier le problème. Essaie de prendre une photo de plus près.")

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
                st.info("Vérifie que ta clé API est bien active sur Google AI Studio.")
