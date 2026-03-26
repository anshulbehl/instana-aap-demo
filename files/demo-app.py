import time
import random
import os
from flask import Flask, jsonify

app = Flask(__name__)
LATENCY_FLAG = "/tmp/simulate-latency"


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/api/checkout")
def checkout():
    if os.path.exists(LATENCY_FLAG):
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)
        return jsonify(status="slow", delay=delay), 200
    time.sleep(random.uniform(0.01, 0.05))
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
