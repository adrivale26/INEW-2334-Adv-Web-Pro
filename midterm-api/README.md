# Midterm API
A RESTful API for creating, reading, updating, and deleting beauty product inventory,
built with Flask and using Flask-SQLAlchemy for database management.

## TECH STACK
* Python
* Flask
* Flask-SQLAlchemy
* SQLite
  
## Project Structure
midterm-api/ <br>
├─.gitignore <br>
├─Beauty_Inventory.db <br>
├─app.py <br>
├─models.py <br>
├─requirements.txt <br>
├─thunder-collection_midterm-api.json <br>
├─seed.py <br>
└─README.md <br>

## How to Run
URL: http://127.0.0.1:5000

## Database Models
### Brand Model
id: integer, primary key <br>
name: string(max 100 characters), required, unique <br>
products: one-to-many relationship <br>
### Product Model
id: integer, primary key <br>
name: string(max 100 characters), required <br>
shade: string(max 100 characters), optional, unique <br>
price: float, required <br>
quantity: integer, required <br>
status: string(max 50 characters), required <br>
brand_id: integer, foreign_key, references brand <br>


### Endpoint Descriptions
### Brands
#### `GET /api/brands`
* Returns all brands with its product count.
* Status code: 200 OK
  
#### `GET /api/brands/brand_id`
* Returns a single brand along with its products.
* Status code: 200 OK
* Error: if brand does not exist: 404 Not Found

#### `POST /api/brands`
* Creates a brand
* Status code: 201 CREATED
* Errors: missing JSON body: 400 Bad Request, missing brand name: 400 Bad Request,
  if brand name is empty or not a string: 422 Unprocessable Entity, if brand name already exists: 409 Conflict
##### Payload Example
{ <br>
   "name": "ColorPop" <br>
} <br>

#### `PUT /api/brands/brand_id`
* Updates brand
* Status code: 200 OK
* Errors :missing JSON body: 400 Bad Request, missing brand name: 400 Bad Request,
  if brand id not found: 404 Not Found

#### `DELETE /api/brands/brand_id`
* Deletes a brand along with its products
* Status code: 200 OK
* Error: if brand id not found: 404 Not Found

### Products
#### `GET /api/products`
* Returns all products and can filter by status
* Status code: 200 OK

#### `GET /api/products/product_id`
* Returns single product
* Status code: 200 OK
* Error: if product id not found: 404 Not Found

#### `POST /api/products`
* Creates a product
* Status code: 201 CREATED
* Errors: missing JSON body: 400 Bad Request, missing fields: 400 Bad Request,
  if brand id not found: 404 Not Found, if product already exists: 409 Conflict, if price is a negative number or not a floating point number: 422 Unprocessable Entity
##### Payload Example
{ <br>
   "name": "Halo Glow Liquid Filter" <br>
   "shade": "3.5 Medium",  <br>
   "price" 15.00,  <br>
   "quantity": 0,  <br>
   "status": "out of stock",  <br>
   "brand_id": 1  <br>
   
} <br>


#### `PUT /api/products/product_id`
* Updates product quantity and status
* Status code: 200 OK
* Errors: missing JSON body: 400 Bad Request, missing fields: 400 Bad Request, if product id not found: 404 Not Found

#### `DELETE /api/products/product_id`
* Deletes a single product
* Status: 200 OK
* Error: if product if not found: 404 Not Found


















