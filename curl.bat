@echo off

:: === CONFIGURATION ===
set "ENDPOINT=https://aicl-mg4fnqyi-eastus2.services.ai.azure.com"
set "DEPLOYMENT=FLUX.1-Kontext-pro"
set "API_VERSION=2025-04-01-preview"
set "API_KEY=60lrcgKn69SDmXuwd00LIjiOJpbQ1YN65Ogeg0EZumGCkvNOajLtJQQJ99BIACHYHv6XJ3w3AAAAACOGdxCZ"
set "IMAGE=image_to_edit.jpg"
set "PROMPT=Make this colored"

:: === APPEL CURL ===
curl -X POST "%ENDPOINT%/openai/deployments/%DEPLOYMENT%/images/edits?api-version=%API_VERSION%" ^
  -H "Authorization: Bearer %API_KEY%" ^
  -F "model=%DEPLOYMENT%" ^
  -F "image=@%IMAGE%" ^
  -F "prompt=%PROMPT%" > response.json

:: === EXTRACTION DE L'IMAGE (si jq et base64 installés) ===
jq -r ".data[0].b64_json" response.json | base64 --decode > edited_image.png

echo ✅ Image générée : edited_image.png
pause
