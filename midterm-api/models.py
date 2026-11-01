from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy import ForeignKey;
db = SQLAlchemy() #creates flask-sqlalchemy extension object

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', backref='brand', cascade='all, delete-orphan')  #establish relationship between models
    
    def to_dict(self, include_products=False):
        data = {"Id": self.id, "Name": self.name}

        if include_products: 
            data["products"] = [p.to_dict() for p in self.products]
        return data

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shade = db.Column(db.String(100), nullable=True, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False) #status of product
    brand_id = db.Column(db.Integer, db.ForeignKey(Brand.id))
   

    def to_dict(self):
        data = {"Id": self.id, "Name": self.name, "Shade": self.shade,
                "Price": self.price, "Quantity": self.quantity, 
                "status": self.status}
        return data

