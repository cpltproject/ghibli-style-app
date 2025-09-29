import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# hop

# === CONFIGURATION AZURE ===
API_KEY = "53RzhbQijGJtsrjraeGCY6ouyyIqMUA1iBVAmPS6WPkj9vTKGWawJQQJ99BIACfhMk5XJ3w3AAAAACOGuZFE"
API_VERSION = "2025-04-01-preview"
DEPLOYMENT = "deploiement-FLUX.1-Kontext-pro"
BASE_URL = "https://projet-flux1-kontext-pr-resource.services.ai.azure.com"
#


GENERATION_URL = f"{BASE_URL}/openai/deployments/{DEPLOYMENT}/images/generations?api-version={API_VERSION}"
EDIT_URL = f"{BASE_URL}/openai/deployments/{DEPLOYMENT}/images/edits?api-version={API_VERSION}"

HEADERS_JSON = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}
HEADERS_FORM = {
    "api-key": API_KEY
}

# === STYLES PRÉDÉFINIS ===
STYLES = [
    "Ghibli", "Pixar", "Van Gogh", "Cyberpunk", "Studio Ghibli aquarelle",
    "Manga noir et blanc", "Renaissance italienne", "Pop Art", "Low Poly", "Synthwave"
]

# === FONCTIONS UTILITAIRES ===
def decode_image(b64_data):
    return Image.open(BytesIO(base64.b64decode(b64_data)))

def generate_image(prompt):
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "output_format": "png"
    }
    response = requests.post(GENERATION_URL, headers=HEADERS_JSON, json=body)
    if response.status_code != 200:
        st.error(f"❌ Erreur génération : {response.text}")
        return None
    return response.json()["data"][0]["b64_json"]

def edit_image(prompt, image_file):
    mime_type = "image/jpeg" if image_file.name.lower().endswith((".jpg", ".jpeg")) else "image/png"
    files = {
        "image": (image_file.name, image_file, mime_type)
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(EDIT_URL, headers=HEADERS_FORM, data=data, files=files)
    if response.status_code != 200:
        st.error(f"❌ Erreur édition : {response.text}")
        return None
    return response.json()["data"][0]["b64_json"]

def offer_download(image, filename):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    st.download_button("📥 Télécharger l’image", buffer.getvalue(), file_name=filename, mime="image/png")

# === INTERFACE STREAMLIT ===
st.set_page_config(page_title="Ghibli Style Generator", page_icon="🎨")
st.title("🎨 Ghibli Style Generator")
st.markdown("Transforme ou stylise tes images avec le modèle FLUX.1-Kontext-pro déployé sur Azure AI Foundry.")

tab1, tab2 = st.tabs(["🚀 Génération sans image", "✏️ Édition d’image existante"])

with tab1:
    with st.form("generation_form"):
        style = st.selectbox("🎨 Choisis un style", STYLES)
        prompt_text = st.text_input("📝 Décris ton image")
        submitted = st.form_submit_button("🚀 Générer")
    if submitted and prompt_text:
        full_prompt = f"{prompt_text}, dans le style {style}"
        b64_img = generate_image(full_prompt)
        if b64_img:
            image = decode_image(b64_img)
            st.image(image, caption=f"Image générée ({style})")
            offer_download(image, f"image_generee_{style}.png")

with tab2:
    with st.form("edit_form"):
        uploaded_file = st.file_uploader("📤 Charge une image", type=["png", "jpg", "jpeg"])
        style_edit = st.selectbox("🎨 Choisis un style", STYLES, key="edit_style")
        edit_prompt_text = st.text_input("📝 Décris la modification")
        edit_submitted = st.form_submit_button("✏️ Modifier")
    if edit_submitted and uploaded_file and edit_prompt_text:
        full_edit_prompt = f"{edit_prompt_text}, dans le style {style_edit}"
        b64_edited = edit_image(full_edit_prompt, uploaded_file)
        if b64_edited:
            image = decode_image(b64_edited)
            st.image(image, caption=f"Image éditée ({style_edit})")
            offer_download(image, f"image_editee_{style_edit}.png")
