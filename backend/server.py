from flask import Flask, request, jsonify
from app.assistant import  handle_user_input, initialize_assistant
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/init", methods=["POST"])
def init():
    print("INIT")
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
    print("ASK")
    data = request.json
    user_input = data.get("message", "")
    print(user_input)

    # Process your virtual assistant logic here
    response = handle_user_input(user_input)
    print(response)
    return jsonify(response)

if __name__ == "__main__":
    print("running")
    app.run(port=5000)