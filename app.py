from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FAQS = {
    "reset password": "To reset your password, click 'Forgot Password' on the login page.",
    "contact support": "You can contact support at support@example.com.",
    "pricing": "Our pricing details are available on the Pricing page of our website."
}

@app.route("/", methods=["GET"])
def home():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"reply": "Invalid input. Please send a JSON payload with a 'message' key."}), 400

    user_input = data["message"]

    for keyword, response in FAQS.items():
        if keyword in user_input.lower():
            return jsonify({"reply": response})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
