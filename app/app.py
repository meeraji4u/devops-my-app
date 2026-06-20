from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Sample App",
        "author": "Balaji K.",
        "hostname": socket.gethostname()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/version")
def version():
    return jsonify({"version": os.environ.get("APP_VERSION", "1.0.0")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
