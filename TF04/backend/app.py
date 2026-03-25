from flask import Flask, jsonify
import os, time, random

app = Flask(__name__)
INSTANCE_ID = os.getenv("INSTANCE_ID", "backend-unknown")
START_TIME = time.time()

PRODUCTS = [
    {"id": 1, "name": "Notebook Pro", "price": 3499.99, "stock": 15},
    {"id": 2, "name": "Mouse Gamer",  "price": 149.90,  "stock": 42},
    {"id": 3, "name": "Teclado Mecânico", "price": 299.90, "stock": 28},
    {"id": 4, "name": "Monitor 24\"", "price": 1199.00, "stock": 10},
    {"id": 5, "name": "Headset USB",  "price": 199.90,  "stock": 35},
]

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "instance_id": INSTANCE_ID})

@app.route("/info")
def info():
    return jsonify({
        "instance_id": INSTANCE_ID,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "load_simulation": round(random.uniform(0.1, 0.9), 2),
    })

@app.route("/products")
def products():
    return jsonify({"instance_id": INSTANCE_ID, "products": PRODUCTS})

@app.route("/products/<int:pid>")
def product(pid):
    p = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "not found"}), 404
    return jsonify({"instance_id": INSTANCE_ID, "product": p})

@app.route("/cart", methods=["GET"])
def cart():
    return jsonify({"instance_id": INSTANCE_ID, "cart": [], "total": 0.0})

@app.route("/status")
def status():
    return jsonify({
        "instance_id": INSTANCE_ID,
        "status": "running",
        "uptime": round(time.time() - START_TIME, 2),
        "requests_served": random.randint(100, 9999),
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
