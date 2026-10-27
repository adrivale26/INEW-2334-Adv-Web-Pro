#imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask import request, jsonify
from flask import Flask

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db' #define location of db
db = SQLAlchemy(app) #creates flask-sqlalchemy extension object and binds to flask app

#create models + define fields + datatypes
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    employees = db.relationship('Employee', backref='department', cascade='all, delete-orphan')  #establish relationship between models


    def to_dictionary(self, include_emp=False): #method that returns a dictionary
        data = {"id": self.id, "name": self.name, "location": self.location}

    #if there are employees include them
        if include_emp:
         data["employees"] = [e.to_dictionary() for e in self.employees]
        return data


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String)
    department_id = db.Column(db.Integer, ForeignKey(Department.id))

    def to_dictionary(self): 
        data = {"id": self.id, "name": self.name, 
            "email": self.email, "role": self.role, "department_id": self.department_id} 
        return data

with app.app_context():
    db.create_all() #creates db

#endpoints + error handlers for departments
@app.route("/api/departments", methods=["GET"])
def get_departments():
    depts = Department.query.all() #similar to SELECT * FROM DEPARTMENT
    return jsonify({"Departments": len(depts),              
    "data": [
        d.to_dictionary(include_emp=True) for d in depts #returns departments + employees
    ]}), 200 

#create department
@app.route("/api/departments", methods=["POST"])
def create_department():
     data = request.get_json() #reads body of the incoming HTTP request and parses it to json returning a python list/dict
     if not data or "name" not in data or "location" not in data:
         return jsonify({"Error Message": "Missing name or missing location"}), 422 #missing field

    #validate if department name is empty
     if not isinstance(data.get("name"), str) or not data["name"].strip():
      return jsonify({"Error Message": "Department name cannot be empty"}), 422

     #check whether data in request already exists, filter by department name
     if Department.query.filter_by(name=data["name"]).first():
      return jsonify ({"Error Message": "Department already exists"}), 409

     dept = Department(name=data["name"], location=data["location"]) #set name + location from data
     db.session.add(dept) #pending insert
     db.session.commit() #applied to db
     return jsonify({"Message": "Department successfully created", "data": dept.to_dictionary()}), 201 #message after department has been created


#get employees
@app.route("/api/employees", methods=["GET"])
def get_employees():
    emp = Employee.query.all() #get all employees
    return jsonify({"Total employees": len(emp), 
                    "Employees": [e.to_dictionary() for e in emp] #get each employee
                    }), 200


#add/create employee 
@app.route("/api/departments/<int:dept_id>/employees", methods=["POST"])
def add_employee(dept_id):
    dept = Department.query.get(dept_id) #get specific dept
    if not dept: #error if dept not found
        return jsonify({"Error Message": f"Department {dept_id} not found"}), 404

    data = request.get_json() #reads body of http request and parses it to json
    if not data or "name" not in data or "role" not in data or "email" not in data: #error if fields are missing
        return jsonify({"Error Message": "Missing name, role, or email"}), 422 #missing field
    
    if not isinstance(data.get("name"), str) or not data["name"].strip():
      return jsonify({"Error Message": "Department name cannot be empty"}), 422
    
    if Employee.query.filter_by(email=data["email"]).first():
        return jsonify ({"Error Message": "Email already exists"}), 409  #email is unique

    
    employ = Employee(name=data["name"], email=data["email"], role=data["role"], department_id=dept_id) #set name, email, & role
    db.session.add(employ) 
    db.session.commit() #commit to db
    return jsonify({"Message": f"Employee successfully added", "data": employ.to_dictionary()}), 201 #message + employee info

#delete department
@app.route("/api/departments/<int:dept_id>", methods=["DELETE"])
def delete_dept(dept_id):
    dept = Department.query.get(dept_id) #get dept
    if not dept:
        return jsonify({"Error Message": f"Department {dept_id} not found"}), 404
    db.session.delete(dept) #delete dept
    db.session.commit()
    return jsonify({"Message": f"Department {dept_id} successfully deleted"}), 200
                       
if __name__ =="__main__":
    app.run(debug=True, port=5002)
