import os
import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")
openai.api_key = OPENAI_API_KEY

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/zoom")
def zoom():
    return render_template("zoom.html")

@app.route("/games")
def games():
    return render_template("games.html")

@app.route("/api/chatbot", methods=["POST"])
def api_chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
