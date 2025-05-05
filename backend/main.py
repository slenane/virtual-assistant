from flask import Flask, request, jsonify
from app.assistant import handle_custom_commands, initialize_assistant
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/init", methods=["POST"])
def init():
    data = request.get_json()
    coords = {
        'lat': data.get('latitude'),
        'lon': data.get('longitude')
    }
    assistant_data = initialize_assistant(coords)
    print(assistant_data)

    return jsonify(assistant_data)

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")

    # Process your virtual assistant logic here
    response = f"You said: {user_input}"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)