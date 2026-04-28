import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration de la page
st.set_page_config(page_title="Dr. Plant", page_icon="🌿", layout="centered")

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez les maladies de vos plantes et trouvez les solutions Jungle Feed.")

# 2. Configuration sécurisée de l'API
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"Erreur de configuration API : {e}")
        st.stop()
else:
    st.error("⚠️ Clé API introuvable. Ajoutez 'GEMINI_API_KEY' dans les Secrets de Streamlit.")
    st.stop()

# 3. Interface de capture
img_file = st.camera_input("Scanner une feuille malade")
if not img_file:
    img_file = st.file_uploader("OU charger une photo depuis la galerie", type=['jpg', 'png', 'jpeg'])

# 4. Analyse
if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Image prête pour l'analyse", use_container_width=True)

    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("L'IA Jungle Feed analyse votre plante..."):
            try:
                # STRATÉGIE ANTI-404 : On cherche le meilleur modèle disponible sur ton compte
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # On définit nos priorités (Flash est plus rapide pour les images)
                priority_list = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro']
                
                selected_model = None
                for target in priority_list:
                    if target in available_models:
                        selected_model = target
                        break
                
                if not selected_model:
                    selected_model = available_models[0] # Fallback sur le premier dispo

                # Exécution du diagnostic
                model = genai.GenerativeModel(selected_model)
                
                prompt = """Tu es l'agronome expert de Jungle Feed. 
                Analyse cette plante. Sois précis et concis.
                1. Diagnostic : Nom de la maladie ou du nuisible.
                2. Cause : Pourquoi c'est arrivé ?
                3. Solutions : Fais un tableau comparatif :
                   - Solution Naturelle (recommande un produit Jungle Feed spécifique).
                   - Solution Classique (produit du commerce ou chimique).
                Sois rassurant et professionnel."""

                response = model.generate_content([prompt, img])
                
                # Affichage du résultat
                st.success(f"✅ Analyse terminée avec succès !")
                st.markdown(response.text)
                st.info(f"Modèle utilisé : {selected_model}")

            except Exception as e:
                st.error("Une erreur technique est survenue.")
                st.expander("Détails de l'erreur pour le support").write(str(e))
                st.info("Conseil : Si l'erreur persiste, créez une nouvelle clé API sur Google AI Studio.")
