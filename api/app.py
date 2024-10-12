from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

app = Flask(__name__)

# Récupérer la clé API depuis les variables d'environnement
API_KEY_LINGVANEX = os.getenv("API_KEY_LINGVANEX")

@app.route('/lingvanex', methods=['POST'])
def translate():
    # Récupérer les données JSON envoyées avec la requête POST
    data = request.get_json()
    text_to_translate = data.get('text', '')  # le texte à traduire
    target_language = data.get('to', 'de_DE')  # langue cible (par défaut l'allemand)

    if not text_to_translate:
        return jsonify({"error": "Text to translate is required"}), 400

    # URL de l'API Lingvanex
    url = "https://api-b2b.backenster.com/b1/api/v3/translate"

    # Payload à envoyer à l'API Lingvanex
    payload = {
        "to": target_language,
        "data": text_to_translate,
        "platform": "api"
    }

    # Headers de la requête, avec l'API key
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": API_KEY_LINGVANEX
    }

    # Envoyer la requête POST à l'API Lingvanex
    response = requests.post(url, json=payload, headers=headers)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Translation failed", "details": response.text}), response.status_code

if __name__ == '__main__':
    # Démarrer le serveur Flask
    app.run(host='0.0.0.0', port=5000)
