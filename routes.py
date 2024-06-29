from flask import render_template, redirect
from forms import AddProduct,  AddAnimals
from forms import Registration, Login
from extensions import app, db
from flask_login import login_user, logout_user, login_required, current_user
import os
from models import Product, ProductCategory, User, Animal



User_list = []

@app.route("/")
def home():
    role = "Admin"
    return render_template("index.html", products=Product.query.all(), role=role)


@app.route("/about")
def about():
    return "About page"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        print(user.email)
        print(form.password.data)
        if user and user.check_password(form.password.data):
            print(user.password)

            login_user(user)
            return redirect("/")
    else:
        print(form.errors)

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    print(current_user.password)
    logout_user()
    return redirect("/")


@app.route("/all_products/<int:category_id>")
@app.route("/all_products")
def all_products(category_id=None):
    if category_id:
        products = ProductCategory.query.get(category_id).products
    else:
        products = Product.query.all()
    return render_template("all_products.html", products=products)


@app.route("/all_animals")
def all_animals():
    animals = Animal.query.all()
    return render_template("all_animals.html", animals=animals)


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


@app.route("/search/<string:product_name>")
def search(product_name):
    products = Product.query.filter(Product.name.ilike(f"%{product_name}%")).all()
    return render_template("all_products.html", products=products)



@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    animals = Animal.query.all()

    if not product:
        return render_template("404.html", id=product_id)

    return render_template("product.html", product=product, animals=animals)


@app.route("/animal/<int:animal_id>")
def animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return render_template("404.html", id=animal_id)

    return render_template("animal.html", animal=animal)



@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = Registration()
    if form.validate_on_submit():
        new_user = User(
            userName=form.userName.data,
            email=form.email.data,
            phone_Number=form.phone_Number.data,
            password=form.password.data,

        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/")
    else:
        print(form.errors)

    return render_template("registration.html", form=form)




@app.route("/add_product", methods = ['POST', 'GET'])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")
    form = AddProduct()


    if form.validate_on_submit():
        #image = form.image.data
        #file_path = os.path.join("static","images", image.filename)
        new_product = Product(name=form.name.data,
                              text=form.text.data,
                              price=form.price.data,
                              image_url=form.image_url.data,
                              category_id=form.category_id.data)



        db.session.add(new_product)
        db.session.commit()

        #image.save(os.path.join(app.root_path, "static","images", image.filename))

    else:
        print(form.errors)


    return render_template("add_product.html", form=form)




@app.route("/add_animal", methods = ['POST', 'GET'])
def add_animal():
    form = AddAnimals()


    if form.validate_on_submit():
        #image = form.image.data
        #file_path = os.path.join("static","images", image.filename)
        new_animal = Animal(animal_name=form.animal_name.data, animal_text=form.animal_text.data, animal_image_url=form.animal_image_url.data)



        db.session.add(new_animal)
        db.session.commit()

        #image.save(os.path.join(app.root_path, "static","images", image.filename))

    else:
        print(form.errors)


    return render_template("add_animal.html", form=form)



@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")


    form = AddProduct(name=product.name, text=product.text, image_url=product.image_url, price=product.price, category_id=product.category_id)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.text = form.text.data
        product.image_url = form.image_url.data
        product.category_id = form.category_id.data



        db.session.commit()
        return redirect("/")



    return render_template("edit_product.html", form=form)


@app.route("/edit_animal/<int:animal_id>", methods=["POST", "GET"])
@login_required
def edit_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return render_template("404.html")


    form = AddAnimals(animal_name=animal.animal_name, animal_text=animal.animal_text, animal_image_url=animal.animal_image_url, )

    if form.validate_on_submit():
        animal.animal_name = form.animal_name.data
        animal.animal_text = form.animal_text.data
        animal.animal_image_url = form.animal_image_url.data



        db.session.commit()
        return redirect("/")



    return render_template("edit_animal.html", form=form)




@app.route("/delete_product/<int:product_id>", methods=["GET", "DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")


    db.session.delete(product)
    db.session.commit()

    return redirect("/")



@app.route("/delete_animal/<int:animal_id>", methods=["GET", "DELETE"])
def delete_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return render_template("404.html")


    db.session.delete(animal)
    db.session.commit()

    return redirect("/")












