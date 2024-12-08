from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Predefined FAQs
FAQS = {
    "reset password": "To reset your password, click 'Forgot Password' on the login page.",
    "contact support": "You can contact support at support@example.com.",
    "pricing": "Our pricing details are available on the Pricing page of our website."
}

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Chatbot API. Use the /chat endpoint to send POST requests.", 200

@app.route("/chat", methods=["POST"])
def chatbot():
    print("Received a request to /chat")

    # Parse the incoming JSON
    data = request.json
    if not data or "message" not in data:
        return jsonify({"reply": "Invalid input. Please send a JSON payload with a 'message' key."}), 400

    user_input = data["message"]
    print(f"User message: {user_input}")

    # Check if the query matches an FAQ
    for keyword, response in FAQS.items():
        if keyword in user_input.lower():
            return jsonify({"reply": response})

    # Handle OpenAI GPT queries
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to a valid model name
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        print(f"OpenAI Reply: {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error while processing OpenAI query: {e}")
        return jsonify({"reply": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
