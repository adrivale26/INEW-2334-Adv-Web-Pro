from flask import Flask, jsonify, request
app = Flask(__name__)
fruits = [
    {"sku": 1, "name": "Strawberries", "price": 2.00},
    {"sku": 2, "name": "Bananas", "price": 1.00},
    {"sku": 3, "name": "Grapes", "price": 3.00}
]

#return health check
@app.route("/api/status", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

#returns array of items and total count
@app.route("/api/fruits", methods=["GET"])
def get_fruits():
    return jsonify({"count": len(fruits), "data": fruits}), 200

#returns the single item matching fruit_sku, if item does not exist, return a message with an error
@app.route("/api/fruits/<int:fruit_sku>", methods=["GET"])
def get_fruit_by_sku(fruit_sku):
    fruit = next((i for i in fruits if i ["sku"] == fruit_sku), None)
    if not fruit:
        return jsonify ({"Error": f"Fruit with Sku {fruit_sku} not found"}), 404
    return jsonify ({"data": fruit}), 200

#accepts JSON payload, validates required field exists
@app.route("/api/fruits", methods=["POST"])
def create_fruit():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"Error": "Invalid payload. 'name' and 'price' are required"}), 400

#append new item with an auto incremented id, return fruit with HTTP 201 Created
#if missing return HTTP 400

    new_sku = max([i["sku"] for i in fruits], default=0) + 1
    new_fruit = {
    "sku": new_sku,
    "name": data["name"],
    "price": data["price"]
    }
    fruits.append(new_fruit)
    return jsonify({"Message": "Fruit created Successfully", "data": new_fruit}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)