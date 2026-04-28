import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration de la page
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿", layout="centered")

st.title("🌿 Dr. Plant : Diagnostic Expert")
st.write("Identifiez les problèmes de vos plantes et découvrez les solutions naturelles Jungle Feed.")

# 2. Configuration de l'IA (Correction 404 incluse)
if "GEMINI_API_KEY" in st.secrets:
    # 'transport=rest' évite les erreurs de version v1beta sur les serveurs européens
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API introuvable. Configurez 'GEMINI_API_KEY' dans les Secrets de Streamlit.")
    st.stop()

# 3. Catalogue de produits exclusif Jungle Feed
CATALOGUE_PRODUITS = """
PRODUITS DISPONIBLES SUR JUNGLEFEED.FR :
- Thrips / Moucherons / Cochenilles : 'Kit Anti-Thrips Ultime' ou 'Anti Thrips & Moucherons Buddies' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles uniquement : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Araignées Rouges : 'Kit Spécial Araignée Rouge' (https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens)
- Moucherons de terreau : 'Kit Anti-Moucherons 3-en-1' (https://www.junglefeed.fr/products/kit-anti-moucherons-3-en-1-naturel)
- Nutrition & Croissance : 'Engrais Plantes d'Intérieur Bio' ou 'Jungle Stick' (https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Soin préventif & Nettoyage : 'Huile de Neem Prête à l'emploi' ou 'Savon Noir' (https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
- Enracinement : 'Eau de Saule Pure' (https://www.junglefeed.fr/products/eau-de-saule-pure-naturelle)
"""

# 4. Interface de capture
img_file = st.camera_input("Prendre une photo de la feuille malade")
if not img_file:
    img_file = st.file_uploader("OU charger une photo depuis votre galerie", type=['jpg', 'png', 'jpeg'])

# 5. Analyse et Diagnostic
if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Image prête pour l'analyse", use_container_width=True)

    if st.button("Lancer le diagnostic 🚀"):
        with st.spinner("L'IA Jungle Feed analyse les cellules de votre plante..."):
            try:
                # Utilisation du modèle le plus stable
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""Tu es l'agronome expert exclusif de la marque Jungle Feed.
                Analyse cette photo de plante pour identifier la maladie, le parasite ou le problème de santé.
                
                CONSIGNES STRICTES :
                1. Donne le nom du diagnostic.
                2. Explique la cause en une phrase simple.
                3. Recommande UNIQUEMENT le produit adapté dans cette liste :
                {CATALOGUE_PRODUITS}
                4. Affiche le lien URL du produit clairement.
                5. Ne cite jamais de marques concurrentes.
                6. Sois expert et encourageant."""

                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("✅ Diagnostic terminé !")
                    st.markdown(response.text)
                    st.balloons()
                else:
                    st.warning("L'IA n'a pas pu générer de texte. Réessayez avec une photo plus nette.")

            except Exception as e:
                st.error(f"Une difficulté technique est survenue : {e}")
                st.info("Astuce : Si l'erreur persiste, essayez de recréer une clé API sur Google AI Studio.")
