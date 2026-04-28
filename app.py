import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration visuelle
st.set_page_config(page_title="Dr. Plant by Jungle Feed", page_icon="🌿")
st.title("🌿 Dr. Plant : Ton Diagnostic Jungle Feed")
st.write("Scanne ta plante, l'IA identifie le problème et te donne la solution naturelle adaptée.")

# 2. Configuration API (via les Secrets Streamlit)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Configuration API manquante dans les Secrets.")
    st.stop()

# 3. Interface de Scan
img_file = st.camera_input("Prendre une photo de la feuille malade")
if not img_file:
    img_file = st.file_uploader("OU choisir une photo dans la galerie", type=['jpg', 'png', 'jpeg'])

# 4. Le Catalogue Jungle Feed (Extrait de ton site)
# Cette liste sert de base de connaissances exclusive à l'IA
CATALOGUE_JUNGLE_FEED = """
- Thrips / Moucherons / Cochenilles : 'Kit Anti-Thrips Ultime' ou 'Anti Thrips & Moucherons Buddies' (Lien : https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
- Cochenilles uniquement : 'Kit Spécial Cochenille' (Lien : https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
- Pucerons : 'Anti-Pucerons Naturel Spray' (Lien : https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
- Araignées Rouges : 'Kit Spécial Araignée Rouge' (Lien : https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens)
- Moucherons de terreau : 'Kit Anti-Moucherons 3-en-1' (Lien : https://www.junglefeed.fr/products/kit-anti-moucherons-3-en-1-naturel)
- Manque de nutrition / Croissance : 'Engrais Plantes d'Intérieur Bio' ou 'Jungle Stick' (Lien : https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml)
- Protection & Soin général : 'Huile de Neem' ou 'Savon Noir' (Lien : https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml)
- Booster Racinaire : 'Eau de Saule' (Lien : https://www.junglefeed.fr/products/eau-de-saule-pure-naturelle)
"""

if img_file is not None:
    img = Image.open(img_file)
    st.image(img, caption="Analyse en cours...", use_container_width=True)
    
    if st.button("Lancer le diagnostic Jungle Feed 🚀"):
        with st.spinner("L'expert Jungle Feed analyse les feuilles..."):
            try:
                # Utilisation du modèle Flash (rapide et efficace)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Le Prompt qui force l'exclusivité
                prompt = f"""Tu es l'agronome expert exclusif de Jungle Feed. 
                Ton but est de vendre les solutions de la boutique.
                
                ANALYSE CETTE IMAGE :
                1. Diagnostic : Identifie précisément la maladie ou le nuisible.
                2. Solution : Recommande UNIQUEMENT un ou plusieurs produits de ce catalogue :
                {CATALOGUE_JUNGLE_FEED}
                
                CONSIGNES STRICTES :
                - Ne propose AUCUNE autre marque.
                - Si la plante n'a rien, propose un 'Jungle Stick' en entretien préventif.
                - Affiche le lien URL du produit de manière très visible.
                - Utilise un ton pro, expert et bienveillant."""

                response = model.generate_content([prompt, img])
                
                st.success("✅ Diagnostic terminé !")
                st.markdown(response.text)
                st.balloons() # Petite animation de succès

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
