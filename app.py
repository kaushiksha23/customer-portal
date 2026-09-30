from flask import Flask, request, jsonify

app = Flask(__name__)

customers = []

@app.route("/")
def home():
    return jsonify({
        "application": "Banking Customer Portal",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/customers", methods=["POST"])
def register_customer():
    data = request.get_json()

    customer = {
        "id": len(customers) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    customers.append(customer)

    return jsonify(customer), 201


@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)