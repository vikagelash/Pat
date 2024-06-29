from extensions import db, app, login_manager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from seed import *


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    image_url = db.Column(db.String)
    text = db.Column(db.String)
    category_id = db.Column(db.ForeignKey("product_category.id"))

    category = db.relationship("ProductCategory")

class ProductCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = db.relationship("Product")


class Animal(db.Model):
    animal_id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String)
    animal_text = db.Column(db.String)
    animal_image_url = db.Column(db.String)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String)
    phone_Number = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, password, userName, email, phone_Number , role="user"):
        self.password = generate_password_hash(password)
        self.userName = userName
        self.email = email
        self.role = role
        self.phone_Number = phone_Number


    def check_password(self, password):
        return check_password_hash(self.password, password)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin = User(email="admin@gmail.com", password="admin123", userName="admin", phone_Number="544566778", role="admin")
        db.session.add(admin)
        db.session.commit()

        for product_category in product_categories:
            new_product_category = ProductCategory()
            new_product_category.name = product_category["name"]

            db.session.add(new_product_category)
            db.session.commit()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)