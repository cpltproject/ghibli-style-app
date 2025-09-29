# Déploiement forcé pour Azure

import streamlit as st
import requests
import base64
from PIL import Image, ImageDraw
from io import BytesIO
import os

# === CONFIGURATION AZURE ===
AZURE_ENDPOINT = "https://ghibli-style-app-csbqbeefd3aueqgb.francecentral-01.azurewebsites.net"
# DEPLOYMENT_NAME = "ghibli-flux"  # ← remplace par le nom réel du déploiement
DEPLOYMENT_NAME = "FLUX.1-Kontext-pro"
API_KEY = os.getenv("API_KEY")   # ← stockée dans App Service
API_VERSION = "2025-04-01-preview"

# === FONCTIONS ===
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def create_mask(size, box):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(box, fill=255)
    return image_to_base64(mask)

def generate_image(image_b64, prompt, mask_b64=None):
    url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/image-generation?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "input": {
            "prompt": prompt,
            "image": image_b64
        }
    }
    if mask_b64:
        payload["input"]["mask"] = mask_b64

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["output"]

# === INTERFACE STREAMLIT ===
st.title("🎨 Style Ghibli avec Azure AI Foundry")
st.markdown("Applique un filtre artistique ou modifie une image avec un prompt IA.")

uploaded_file = st.file_uploader("📤 Charge ton image", type=["jpg", "jpeg", "png"])
prompt = st.text_area("📝 Ton prompt", "Transform this image into Studio Ghibli style with soft lighting.")

use_mask = st.checkbox("🎯 Utiliser une zone ciblée (masque)", value=False)

if use_mask:
    x1 = st.slider("🧭 X début", 0, 1024, 100)
    y1 = st.slider("🧭 Y début", 0, 1024, 300)
    x2 = st.slider("🧭 X fin", 0, 1024, 300)
    y2 = st.slider("🧭 Y fin", 0, 1024, 600)

if uploaded_file and st.button("🚀 Générer l’image stylisée"):
    image = Image.open(uploaded_file).resize((1024, 1024))
    image_b64 = image_to_base64(image)
    mask_b64 = create_mask((1024, 1024), (x1, y1, x2, y2)) if use_mask else None

    with st.spinner("Génération en cours..."):
        result_b64 = generate_image(image_b64, prompt, mask_b64)
        result_img = Image.open(BytesIO(base64.b64decode(result_b64)))
        st.image(result_img, caption="✅ Image stylisée", use_column_width=True)

# Déploiement forcé pour Azure
