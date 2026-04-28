import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration
st.set_page_config(page_title="Dr. Plant", page_icon="🌿")
st.title("🌿 Dr. Plant : Diagnostic Expert")

# --- RÉCUPÉRATION DE LA CLÉ ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# --- INTERFACE ---
img_file = st.camera_input("Prendre une photo de la feuille")
if not img_file:
    img_file = st.file_uploader("OU choisir une photo", type=['jpg', 'png', 'jpeg'])

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Plante à analyser", use_container_width=True)
    
    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("Analyse en cours par l'IA..."):
            # Liste des noms de modèles à tester par ordre de priorité
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest']
            success = False
            
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = "Analyse cette plante : Diagnostic, Cause, et Tableau (Solution Naturelle Jungle Feed vs Solution Classique)."
                    response = model.generate_content([prompt, img])
                    
                    if response.text:
                        st.success(f"✅ Diagnostic terminé (Modèle : {model_name})")
                        st.markdown(response.text)
                        success = True
                        break # On a réussi, on sort de la boucle
                except Exception as e:
                    continue # Si ça échoue, on tente le suivant
            
            if not success:
                st.error("Désolé, l'IA ne répond pas. Vérifie que ta clé API est valide et n'a pas expiré.")
