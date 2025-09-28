python
import streamlit as st
import requests
import base64
from PIL import Image, ImageDraw
from io import BytesIO

# === CONFIGURATION AZURE ===
AZURE_ENDPOINT = "https://<TON-NOM-DE-RESSOURCE>.openai.azure.com"
DEPLOYMENT_NAME = "<TON-NOM-DE-DÉPLOIEMENT>"
API_KEY = "<TA-CLÉ-API>"
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

def edit_image(image_b64, mask_b64, prompt):
    url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/images/edits?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    payload = {
        "image": image_b64,
        "mask": mask_b64,
        "prompt": prompt,
        "model": "gpt-image-1",
        "size": "1024x1024",
        "n": 1,
        "quality": "high"
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["data"][0]["image"]

# === INTERFACE STREAMLIT ===
st.title("🖼️ Retouche IA avec Azure OpenAI")
st.markdown("Ajoute un bras à Churchill ou modifie n’importe quelle image avec un prompt IA.")

uploaded_file = st.file_uploader("📤 Charge ton image", type=["jpg", "jpeg", "png"])
prompt = st.text_area("📝 Ton prompt", "Add a third arm to Winston Churchill on the left side, making the V for Victory sign.")

x1 = st.slider("🧭 X début", 0, 1024, 100)
y1 = st.slider("🧭 Y début", 0, 1024, 300)
x2 = st.slider("🧭 X fin", 0, 1024, 300)
y2 = st.slider("🧭 Y fin", 0, 1024, 600)

if uploaded_file and st.button("🎨 Générer l’image modifiée"):
    image = Image.open(uploaded_file).resize((1024, 1024))
    image_b64 = image_to_base64(image)
    mask_b64 = create_mask((1024, 1024), (x1, y1, x2, y2))

    with st.spinner("Génération en cours..."):
        result_b64 = edit_image(image_b64, mask_b64, prompt)
        result_img = Image.open(BytesIO(base64.b64decode(result_b64)))
        st.image(result_img, caption="✅ Image modifiée", use_column_width=True)
