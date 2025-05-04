from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")

    # Process your virtual assistant logic here
    response = f"You said: {user_input}"
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)