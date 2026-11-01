from flask import Flask, jsonify, request
from models import db, Brand, Product
import os
app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #locates folder containing app.py
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "Beauty_Inventory.db") #location of db + use abs path 
db.init_app(app)
with app.app_context():
    db.create_all()
#custom error handlers

#get brands 
@app.route("/api/brands", methods=["GET"])
def get_brands():
    brands = Brand.query.all() #SELECT * FROM BRAND
    return jsonify ([
        {"Id": b.id, "Brand": b.name, "Number of products": len(b.products)}
        for b in brands
        ]), 200

#get single brand 
@app.route("/api/brands/<int:brand_id>", methods=["GET"])
def get_single_brand(brand_id):
    brand = Brand.query.get(brand_id) #SELECT * FROM BRAND WHERE ID matches
    if not brand:
        return jsonify({"Error": f"Brand Id {brand_id} not found"}), 404
    products = [ 
        {"Id": p.id, "Name": p.name, "Shade": p.shade, "Price": p.price,
         "Quantity": p.quantity, "Status": p.status
         } for p in brand.products
    ]
    return jsonify({
        "Id": brand.id,
        "Name": brand.name,
        "Products": products
        }), 200
    

#add brands
@app.route("/api/brands", methods=["POST"])
def add_brand():
   data = request.get_json() 
   if not data: 
         return jsonify({"Error Msg": "Missing JSON request body"}), 400
   if not data or not "name" in data:
       return jsonify ({"Error": "Missing brand name"}), 400
   if not isinstance(data.get("name"), str) or not data["name"].strip():
        return jsonify({"Error": "Brand name must be a string or cannot be empty"}), 422
   if Brand.query.filter_by(name=data["name"]).first():
         return jsonify ({"Error Message": "Brand already exists"}), 409

   brand = Brand(name=data["name"]) #set name
   db.session.add(brand) 
   db.session.commit() #commit 
   return jsonify({"Message": "Brand successfully added."}), 201

#update brand
@app.route("/api/brands/<int:brand_id>", methods=["PUT"])
def update_brand(brand_id):
    data = request.get_json() 
    brand = Brand.query.get(brand_id)
    if not data: 
          return jsonify({"Error": "Missing JSON request body"}), 400
    if not "name" in data:
        return jsonify ({"Error": "Missing brand name"}), 400
    if not brand:
            return jsonify({"Error": f"Brand Id {brand_id} not found"}), 404
    if not isinstance(data.get("name"), str) or not data["name"].strip():
       return jsonify({"Error": "Brand name must be a string or cannot be empty"}), 422
    

    brand.name = data["name"] #set name
    db.session.add(brand) 
    db.session.commit() #commit 
    return jsonify({"Message": "Brand successfully updated."}), 200

#delete brand
@app.route("/api/brands/<int:brand_id>", methods=["DELETE"])
def delete_brand(brand_id):
    brand = Brand.query.get(brand_id) #get brand id
    if not brand:
        return jsonify({"Error": f"Brand {brand_id} was not found."}), 404
    db.session.delete(brand)
    db.session.commit()
    return jsonify({"Message": f"Brand {brand_id} successfully deleted along with brand {brand_id} products"}), 200


#list all products 
@app.route("/api/products", methods=["GET"])
def get_products():
    status = request.args.get("status")
    query = Product.query #all products
    if status:
        query = query.filter(Product.status == status) #filter by status
    products = query.all() 
    return jsonify([
        {"Id": p.id, "Name": p.name, "Shade": p.shade, "Price": p.price,
         "Quantity": p.quantity, "Status": p.status}
         for p in products
    ]), 200 

#get single product using id
@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_single_product(product_id):
    product = Product.query.get(product_id) 
    if not product: 
        return jsonify({"Error": f"Product {product_id} was not found"}), 404
    return jsonify(
        {"Id": product.id, "Name": product.name, "Shade": product.shade, "Price": product.price,
            "Quantity": product.quantity, "Status": product.status }), 200

#add product
@app.route("/api/products", methods=["POST"])
def add_product():
     data = request.get_json() 
     if not data: 
           return jsonify({"Error": "Missing JSON request body"}), 400
     required_fields = ["name","shade","price","quantity", "status", "brand_id"]
     for field in required_fields: #loop over fields and check if fields are missing
        if not data or field not in data:
         return jsonify({"Error": f"Missing {field} field"}), 400
     brand = Brand.query.get(data["brand_id"]) #reads id client sent
     if not brand:
        return jsonify({"Error": "Brand not found"}), 404
     
     if Product.query.filter_by(shade=data["shade"]).first(): #shade name is unique
        return jsonify ({"Error": "Product already exists"}), 409
     
     if not isinstance(data.get("price"), float):
             return jsonify({"Error": "Price must be a floating point number"}), 422
     if data["price"] < 0:
         return jsonify({"Error": "Price cannot be a negative number"}), 422 #check if number is a float + if its a negative value
     product = Product(name=data["name"], shade=data["shade"], price=data["price"],
                       quantity=data["quantity"], status=data["status"], brand_id=data["brand_id"]) #set fields
     db.session.add(product)
     db.session.commit()
     return jsonify({"Message": "Product successfully added"}), 201

#update product quantity + status
@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json() 
    if not data: 
          return jsonify({"Error": "Missing JSON request body"}), 400
    product = Product.query.get(product_id)
    if not product: 
        return jsonify({"Error": f"Product {product_id} was not found"}), 404
    if not "quantity" in data or not "status" in data:
        return jsonify ({"Error": "Missing quantity or status"}), 400
    product.quantity = data["quantity"] #update quantity
    product.status = data["status"] #update status
    db.session.commit()
    return jsonify({"Message": "Product details successfully updated"}), 200

#delete single item
@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)  #get product id
    if not product:
        return jsonify({"Error": f"Product {product_id} not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"Message": f"Product {product_id} successfully deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)