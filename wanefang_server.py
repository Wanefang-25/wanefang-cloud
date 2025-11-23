from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env for local dev
load_dotenv(override=True)

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load persona / character bible from file
with open("wanefang_character_bible.txt", "r", encoding="utf-8") as f:
    WANEFANG_PERSONA = f.read()

# Create OpenAI client using API key from environment
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/")
def index():
    # Serve the HTML chat UI
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    # Call OpenAI with Wanefang persona + user message
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": WANEFANG_PERSONA},
            {"role": "user", "content": user_message},
        ],
    )

    reply = resp.choices[0].message.content
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)

