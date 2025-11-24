from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# ------------------------------------------------------
# Paths & environment
# ------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = BASE_DIR / ".env"

# Load .env for local dev (Render uses dashboard ENV instead)
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        f"OPENAI_API_KEY is not set. If running locally, create {DOTENV_PATH} with:\n"
        f"OPENAI_API_KEY=sk-proj-xxxx"
    )

client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------------------------------------
# Load persona
# ------------------------------------------------------

PERSONA_PATH = BASE_DIR / "wanefang_character_bible.txt"

if PERSONA_PATH.exists():
    WANEFANG_PERSONA = PERSONA_PATH.read_text(encoding="utf-8")
else:
    WANEFANG_PERSONA = (
        "You are Wanefang, the mystical dragon librarian of The Behr Cave. "
        "You speak in a warm, poetic, cosmic tone, mixing wisdom with wonder."
    )

# ------------------------------------------------------
# Flask app
# ------------------------------------------------------

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    template_folder=str(BASE_DIR / "templates"),
)

@app.route("/", methods=["GET"])
def index():
    """Serve the main HTML page with the dragon and chat box."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Accept JSON {message: "..."} and return {reply: "..."}."""
    data = request.get_json(force=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": WANEFANG_PERSONA},
                {"role": "user", "content": user_message},
            ],
        )

        reply = resp.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Basic health check for Render and debugging."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)

