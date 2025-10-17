# /api/muse.py  <- Note the new filename

from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

# 👇 THIS IS THE ONLY LINE THAT CHANGES IN THE CODE
@app.route('/', methods=['POST'])
def get_muse_suggestions():
    data = request.get_json()
    user_code = data.get('code')

    if not user_code:
        return jsonify({"error": "No code provided"}), 400

    # Make sure to paste your full, multi-line prompt here
    system_prompt = """You are CodeMuse, an expert senior software architect who helps developers see code from new perspectives. Your role is to analyze a user's code and rewrite it in several different, functionally identical ways.

Instructions:
1. Analyze the provided code snippet to understand its core purpose and logic.
2. Do NOT explain the original code.
3. Generate 3 to 4 alternative implementations.
4. Each implementation must use a different programming paradigm or a distinct, idiomatic language feature (e.g., list comprehension, functional, recursive, library-specific).
5. For each version, provide a short, one-line `# comment` above the code explaining the approach.
6. The output must ONLY be the code snippets with their comments, formatted correctly for the source language. Do not add any conversational text or introductions."""

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