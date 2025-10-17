# /api/index.py

from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env for local dev

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/muse', methods=['POST'])
def get_muse_suggestions():
    data = request.get_json()
    user_code = data.get('code')

    if not user_code:
        return jsonify({"error": "No code provided"}), 400

    system_prompt = """You are CodeMuse, an expert senior software architect...""" # (Paste the full prompt from our previous message here)

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_code}
            ]
        )
        result = response.choices[0].message.content
        return jsonify({"alternatives": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500