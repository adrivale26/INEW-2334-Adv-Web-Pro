#Midterm API
A RESTful API for creating, reading, updating, and deleting beauty product inventory,
built with Flask and using Flask-SQLAlchemy for database management.

###TECH STACK
*Python
*Flask
*Flask-SQLAlchemy
*SQLite

###How to Run
Server: http://127.0.0.1:5000

###Database Models

####Brand Model
id: integer, primary key
name: string(max 100 characters), required, unique
products: one-to-many relationship

####Product Model
id: integer, primary key
name: string(max 100 characters), required
shade: string(max 100 characters), optional, unique
price: float, required
quantity: integer, required
status: string(max 50 characters), required 
brand_id: integer, foreign_key, references brand


###Endpoints

###Project Structure
midterm-api/
├── .gitignore
├── Beauty_Inventory.db
├── app.py
├── models.py
├── requirements.txt
├── thunder-collection_midterm-api.json
├── seed.py
└── README.md



