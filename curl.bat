@echo off

:: === CONFIGURATION ===
set "ENDPOINT=https://projet-flux1-kontext-pr-resource.services.ai.azure.com"
set "DEPLOYMENT=deploiement-FLUX.1-Kontext-pro"
set "API_VERSION=2025-04-01-preview"
set "API_KEY=60lrcgKn69SDmXuwd00LIjiOJpbQ1YN65Ogeg0EZumGCkvNOajLtJQQJ99BIACHYHv6XJ3w3AAAAACOGdxCZ"
set "IMAGE=image_to_edit.jpg"
set "PROMPT=Make this colored"

:: === VÉRIFICATION DE L'IMAGE ===
if not exist "%IMAGE%" (
    echo ❌ Fichier image introuvable : %IMAGE%
    pause
    exit /b
)

:: === APPEL CURL ===
curl --max-time 30 -X POST "%ENDPOINT%/openai/deployments/%DEPLOYMENT%/images/generations?api-version=%API_VERSION%" ^
  -H "Authorization: Bearer %API_KEY%" ^
  -F "model=%DEPLOYMENT%" ^
  -F "image=@%IMAGE%" ^
  -F "prompt=%PROMPT%" ^
  2>&1 > response.json

:: === AFFICHAGE DE LA RÉPONSE POUR DEBUG ===
type response.json

:: === EXTRACTION DE L'IMAGE (si jq et base64 installés) ===
jq -r ".data[0].b64_json" response.json | base64 --decode > edited_image.png

echo ✅ Image stylisée générée : edited_image.png
pause
