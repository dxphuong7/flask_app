# app.py
from flask import Flask, jsonify, request
from config import get_config
import os

app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# ✅ Home route
@app.route("/")
def home():
    return jsonify({
        "app": "Flask Calculator MVP",
        "env": os.getenv("FLASK_ENV"),
        "status": "running"
    })

# ✅ Calculator route
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    op = data.get("operator")

    if a is None or b is None or op is None:
        return jsonify({"error": "Missing a, b, or operator"}), 400

    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                return jsonify({"error": "Cannot divide by zero"}), 400
            result = a / b
        else:
            return jsonify({"error": "Invalid operator"}), 400

        return jsonify({
            "a": a,
            "operator": op,
            "b": b,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Config route (only in development)
@app.route("/config")
def config_info():
    if not app.config["DEBUG"]:
        return jsonify({"error": "Not available in production"}), 403
    return jsonify({
        "env": os.getenv("FLASK_ENV"),
        "debug": app.config["DEBUG"],
        "database": os.getenv("DATABASE_URL"),
        "port": os.getenv("PORT"),
        "api_key": os.getenv("API_KEY")[:6] + "..." if os.getenv("API_KEY") else None
    })

# ✅ Health check route (useful for Render)
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "env": os.getenv("FLASK_ENV")
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Starting Flask on port {port}...")
    print(f"Environment: {os.getenv('FLASK_ENV')}")
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])