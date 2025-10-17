# /api/index.py

from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)

# Set the API key from the environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/muse', methods=['POST'])
def get_muse_suggestions():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"error": "No code provided"}), 400
    
    user_code = data['code']

    # This is our refined "Master Prompt"
    system_prompt = """
    You are CodeMuse, an expert senior software architect who helps developers see code from new perspectives. Your role is to analyze a user's code and rewrite it in several different, functionally identical ways.

    Instructions:
    1. Analyze the provided code snippet to understand its core purpose and logic.
    2. Do NOT explain the original code.
    3. Generate 3 to 4 alternative implementations.
    4. Each implementation must use a different programming paradigm or a distinct, idiomatic language feature (e.g., list comprehension, functional, recursive, library-specific).
    5. For each version, provide a short, one-line `# comment` above the code explaining the approach.
    6. The output must ONLY be the code snippets with their comments, formatted correctly for the source language. Do not add any conversational text or introductions.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4", # Use "gpt-3.5-turbo" if you don't have GPT-4 API access
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_code}
            ]
        )
        result = response.choices[0].message.content
        return jsonify({"alternatives": result})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to communicate with AI service."}), 500