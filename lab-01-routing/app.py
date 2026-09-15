from flask import Flask, jsonify, request

#the class 
app = Flask (__name__)

fruits = [
    {"sku": 1, "name": "Strawberries", "price": 2.00},
    {"sku": 2, "name": "Bananas", "price": 1.50},
    {"sku": 3, "name": "Grapes", "price": 1.50}

]

#returns a health-check JSON payload
@app.route("/api/status", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

#returns full array of items + total count + status of 200
@app.route("/api/fruits", methods=["GET"])
def get_fruits():
    return jsonify({"count": len(fruits), "data": fruits}), 200

#returns single fruit matching fruit_sku, if item does not match return error message + 404
@app.route("/api/fruits/<int:fruit_sku>", methods=["GET"])
def get_fruit_by_sku(fruit_sku):
    fruit = next((i for i in fruits if i["sku"] == fruit_sku), None)
    if fruit is None: 
        return jsonify(
            {"error": "Fruit not Found", 
             "fruit_sku": fruit_sku
             }), 404
    return jsonify({"data": fruit}), 200
    
@app.route("/api/fruits", methods=["POST"])
def create_fruit():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid payload. 'name' and 'price' are required."}), 404

    new_sku = max([i["sku"] for i in fruits], default=0) + 1
    new_fruit = {
        "sku": new_sku,
        "name": data["name"],
        "price": data["price"]
    }
    fruits.append(new_fruit)
    return jsonify({"message": "Fruit created successfully", "data": new_fruit}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)


