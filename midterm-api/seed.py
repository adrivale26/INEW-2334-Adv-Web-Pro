from app import app, db
from models import Brand, Product

with app.app_context():
 db.drop_all() #wipes old data + tables 
 db.create_all() #rebuilds tables from your models

 b1 = Brand(name="e.l.f Cosmetics")
 b2 = Brand(name="NYX")
 b3 = Brand(name="Nars")

 db.session.add_all([b1, b2, b3])
 db.session.commit() #commit 

 p1 = Product(name="Power Grip Primer", price=11.00, quantity= 35, status="in stock", brand_id=b1.id)
 p2 = Product(name="Glow Reviver Lip Oil", shade="Jam Session", price=9.00, quantity= 50, status="in stock", brand_id=b1.id)

 p3 = Product(name="Slim Lip Pencil Lip Liner", shade="Mauve", price=5.99, quantity= 0, status="out of stock", brand_id=b2.id)
 p4 = Product(name="Buttermelt Glaze Skin Tint SPF 30", shade="Vanilla Bean Butta", price=16.00, quantity= 8, status="in stock", brand_id=b2.id)

 p5 = Product(name="Light Reflecting Foundation", shade="Valencia", price=55.00, quantity= 18, status="in stock", brand_id=b3.id)
 p6 = Product(name="Radiant Creamy Concealer", shade="Madeleine", price=36.00, quantity= 24, status="in stock", brand_id=b3.id)
 

 db.session.add_all([p1, p2, p3, p4, p5, p6])
 db.session.commit()

 print("Database seeded successfully with initial records.")


