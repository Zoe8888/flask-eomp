# Importing various modules
import hmac
import sqlite3
import datetime
import cloudinary
import cloudinary.uploader
import validate_email
import DNS
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required
from flask_cors import CORS


# Creating a user class
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Creating a product class
class Product(object):
    def __init__(self, product_id, product_name, product_image, category, description, dimensions, price):
        self.product_id = product_id
        self.product = product_name
        self.product_image = product_image
        self.category = category
        self.description = description
        self.dimensions = dimensions
        self.price = price


# Creating a database class
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('pos.db')
        self.cursor = self.conn.cursor()

    def registration(self, name, surname, email, username, password):
        self.cursor.execute("INSERT INTO user(name, surname, email, username, password) VALUES (?, ?, ?, ?, ?)"
                            , (name, surname, email, username, password))
        self.conn.commit()

    def edit_profile(self, incoming_data, id):
        response = {}
        put_data = {}

        if incoming_data.get('name') is not None:
            put_data['name'] = incoming_data.get('name')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET name =? WHERE id =?", (put_data['name'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Name successfully updated"

        if incoming_data.get('surname') is not None:
            put_data['surname'] = incoming_data.get('surname')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET surname =? WHERE id=?", (put_data['surname'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Surname successfully updated"

        if incoming_data.get('email') is not None:
            put_data['email'] = incoming_data.get('email')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET email =? WHERE id=?", (put_data['email'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "ID number successfully updated"

        if incoming_data.get('username') is not None:
            put_data['username'] = incoming_data.get('username')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET username =? WHERE id=?", (put_data['username'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Username successfully updated"

        if incoming_data.get('password') is not None:
            put_data['password'] = incoming_data.get('password')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE user SET password =? WHERE id=?", (put_data['password'], id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Password successfully updated"

        return response


    def delete_profile(self, value):
        query = ("DELETE FROM user WHERE id='{}'".format(value))
        self.cursor.execute(query)
        self.conn.commit()

    def add_product(self, product_name, product_image, category, description, dimensions, price, id):
        cloudinary.config(cloud_name='dxgylrfai', api_key='297452228378499', api_secret='lMfu9nSDHtFhnaRTiEch_gfzm_A')
        upload_result = None
        app.logger.info('%s file_to_upload', product_image)
        if product_name:
            upload_result = cloudinary.uploader.upload(product_image)
            app.logger.info(upload_result)
        self.cursor.execute("INSERT INTO product (product_name, product_image, category, description, dimensions, "
                            "price, id) VALUES(?, ?, ?, ?, ?, ?, ?)",
                            (product_name, upload_result['url'], category, description, dimensions, price, id))
        self.conn.commit()

    def edit_product(self, incoming_data, product_id):
        response = {}
        put_data = {}

        if incoming_data.get('product_name') is not None:
            put_data['product_name'] = incoming_data.get('product_name')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_name =? WHERE product_id=?", (put_data['product_name'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Product name was successfully updated."

        if incoming_data.get('product_image') is not None:
            put_data['product_image'] = incoming_data.get('product_image')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product_image =? WHERE product_id=?", (put_data['product_image'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Product image was successfully updated."

        if incoming_data.get('category') is not None:
            put_data['category'] = incoming_data.get('category')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET category =? WHERE product_id=?", (put_data['category'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Category successfully updated."

        if incoming_data.get('description') is not None:
            put_data['description'] = incoming_data.get('description')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET description =? WHERE product_id=?",
                               (put_data['description'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Description was successfully updated."

        if incoming_data.get('dimensions') is not None:
            put_data['dimensions'] = incoming_data.get('dimensions')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET dimensions=? WHERE product_id=?",
                               (put_data['dimensions'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Dimensions was successfully updated."

        if incoming_data.get('price') is not None:
            put_data['price'] = incoming_data.get('price')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET price=? WHERE product_id=?",
                               (put_data['price'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Price was successfully updated."

        if incoming_data.get('id') is not None:
            put_data['id'] = incoming_data.get('id')

            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET id=? WHERE product_id=?",
                               (put_data['id'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "ID was successfully updated."

        return response

    def delete_product(self, value):
        query = ("DELETE FROM product WHERE product_id='{}'".format(value))
        self.cursor.execute(query)
        self.conn.commit()

    def show_products(self):
        query = ("SELECT * FROM product")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def view_product(self, value):
        query = ("SELECT * FROM product WHERE product_id='{}'".format(value))
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        return response

    def view_users_products(self, value):
        query = ("SELECT * FROM product WHERE id='{}'".format(value))
        self.cursor.execute(query)
        return  self.cursor.fetchall()


# Creating a user table
def init_user_table():
    conn = sqlite3.connect('pos.db')
    print('Opened database successfully.')

    conn.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("User table created successfully")
    conn.close()


# Creating a product table
def init_product_table():
    with sqlite3.connect('pos.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "product_name TEXT NOT NULL, product_image TEXT NOT NULL, category TEXT NOT NULL, "
                     "description TEXT NOT NULL, dimensions TEXT NOT NULL, price TEXT NOT NULL, id INTEGER NOT NULL,"
                     "FOREIGN KEY (id) REFERENCES user(id))")
        print("Product table created successfully.")


# Fetching all users
def fetch_users():
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[4], data[5]))
    return new_data


# Fetching all products
def fetch_products():
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        new_product = []

        for data in products:
            new_product.append(Product(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    return new_product


# def init_cart_table():
#     with sqlite3.connect('pos.db') as conn:
#         conn.execute("CREATE TABLE IF NOT EXISTS cart (product_id INTEGER FOREIGN KEY)")

init_user_table()
init_product_table()
users = fetch_users()
products = fetch_products()


username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    id = payload['identity']
    return userid_table.get(id, None)


# App initialized
app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# Extends the jwt tokens validation time to 20 hours
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=20)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# Senders email
app.config['MAIL_USERNAME'] = 'ifyshop965@gmail.com'
# Senders password
app.config['MAIL_PASSWORD'] = 't3amShopify'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

jwt = JWT(app, authenticate, identity)


# User registration route and function
@app.route('/registration/', methods=["POST"])
def registration():
    db = Database()
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username='{}'".format(username))
            registered_username = cursor.fetchone()

        if name == '' or surname == '' or email == '' or username == '' or password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter all fields."
            return response

        if not validate_email.validate_email(email, verify=True):
            response['status_code'] = 400
            response['message'] = "Error! Please enter a valid email address."

        if registered_username:
            response['username'] = username
            response['status_code'] = 400
            response['message'] = "Username already taken. Please enter a unique username."
            return response

        db.registration(name, surname, email, username, password)

        mail = Mail(app)
        msg = Message("Welcome!", sender='ifyshop965@gmail.com', recipients=[email])
        msg.body = "Good morning/afternoon {}.\n".format(name)
        msg.body = msg.body + "Your have successfully registered your profile on our site with the username {}.\n"\
            .format(username)
        msg.body = msg.body + "Please feel free to send us email if you have any queries or concerns.\n \n" \
                              "Kind regards,\n Shopify Team"
        mail.send(msg)

        response["message"] = "New user successfully registered"
        response["status_code"] = 200
        return response


# User login route and function
@app.route('/login/', methods=["POST"])
def login():
    response = {}

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
            registered_user = cursor.fetchone()

        if username == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your username."
            return response

        if password == '':
            response['status_code'] = 400
            response['message'] = "Error! Please enter your password."
            return response

        if registered_user:
            response['registered_user'] = registered_user
            response['status_code'] = 200
            response['message'] = "Successfully logged in"
            return response

        else:
            response['status_code'] = 400
            response['message'] = "Login unsuccessful. Please try again."
        return jsonify(response)


# Display all users route anf function
@app.route('/display-users/', methods=["GET"])
def display_users():
    response = {}
    with sqlite3.connect("pos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        all_users = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = all_users
    return response


# View specific users profile route and function
@app.route('/view-profile/<int:id>/', methods=["GET"])
@jwt_required()
def view_profile(id):
    response = {}

    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id=?", (str(id)))

        response['status_code'] = 200
        response['message'] = "Profile retrieved successfully"
        response['data'] = cursor.fetchone()

    return jsonify(response)


# Edit users profile route and function
@app.route('/edit-profile/<int:id>/', methods=["PUT"])
@jwt_required()
def edit_profile(id):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        response = db.edit_profile(incoming_data, id)

    return response



# Delete a users profile route and function
@app.route('/delete-profile/<int:id>')
def delete_profile(id):
    response = {}
    db = Database()
    db.delete_profile(id)
    response['status_code'] = 200
    response['message'] = "Profile successfully deleted"
    return response


# Adding a new product route and function
@app.route('/add-product/', methods=["POST"])
@jwt_required()
def add_product():
    db = Database()
    response = {}

    if request.method == "POST":
        product_name = request.form['product_name']
        product_image = request.files['product_image']
        category = request.form['category']
        description = request.form['description']
        dimensions = request.form['dimensions']
        price = request.form['price']
        id = request.form['id']

        db.add_product(product_name, product_image, category, description, dimensions, price, id)
        response["status_code"] = 201
        response['description'] = "Product added successfully"
        return response


# Deleting a specific product route and function
@app.route('/delete-product/<int:product_id>')
@jwt_required()
def delete_product(product_id):
    db = Database()
    response = {}
    db.delete_product(product_id)
    response['status_code'] = 200
    response['message'] = "Product successfully deleted"
    return response


# Editing a specific product route and function
@app.route('/edit-product/<int:product_id>/', methods=["PUT"])
@jwt_required()
def edit_product(product_id):
    response = {}

    if request.method == "PUT":
        incoming_data = dict(request.json)
        db = Database()
        response = db.edit_product(incoming_data, product_id)

    return response


# Display all products route and function
@app.route('/show-products/', methods=["GET"])
@jwt_required()
def show_products():
    db = Database()
    response = {}

    products = db.show_products()
    response['status_code'] = 200
    response['data'] = products
    return response


# View a specific product route and function
@app.route('/view-product/<int:product_id>', methods=["GET"])
@jwt_required()
def view_product(product_id):
    db = Database()
    response = {}

    data = db.view_product(product_id)
    response['data'] = data
    response['status_code'] = 200
    response['description'] = "Product was successfully retrieved"

    return jsonify(response)


# View a specifics users products route and function
@app.route('/view-user-products/<int:id>/', methods=["GET"])
@jwt_required()
def view_user_products(id):
    response = {}
    db = Database()

    user_products = db.view_users_products(id)
    response['status_code'] = 200
    response['message'] = "All products from user retrieved successfully"
    response['data'] = user_products

    return response


if __name__ == '__main__':
    app.run()
