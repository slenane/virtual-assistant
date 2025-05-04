from flask import Flask, request, jsonify
from app.assistant import handle_custom_commands, get_greeting
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/init", methods=["GET"])
def init():
    greeting = get_greeting()
    print(greeting)

    return jsonify({"response": greeting})

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")

    # Process your virtual assistant logic here
    response = f"You said: {user_input}"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)