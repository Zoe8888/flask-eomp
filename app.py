import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def fetch_users():
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[4], data[5]))
    return new_data


def init_user_table():
    conn = sqlite3.connect('pos.db')
    print('Opened database successfully.')

    conn.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name TEXT NOT NULL, surname TEXT NOT NULL, id_number TEXT NOT NULL, username TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("User table created successfully")
    conn.close()


def init_product_table():
    with sqlite3.connect('pos.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "product TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, "
                     "dimensions TEXT NOT NULL, price TEXT NOT NULL)")
        print("Product table created successfully.")


def init_cart_table():
    with sqlite3.connect('pos.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS cart (product_id INTEGER FOREIGN KEY)")


init_user_table()
init_product_table()
users = fetch_users()

username_table = { u.username: u for u in users }
userid_table = { u.id: u for u in users }


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    id = payload['identity']
    return userid_table.get(id, None)


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/registration/', methods=["POST"])
def registration():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        id_number = request.form['id_number']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user(name, surname, id_number, username, password) VALUES (?, ?, ?, ?, ?)",
                           (name, surname, id_number, username, password))
            conn.commit()
            response["message"] = "New user successfully registered"
            response["status_code"] = 201
        return response


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

        if registered_user:
            response['registered_user'] = registered_user
            response['status_code'] = 200
            response['message'] = "Successfully logged in"

        else:
            response['status_code'] = 401
            response['message'] = "Login unsuccessful. Please try again."
        return jsonify(response)


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


@app.route('/edit-profile/<int:id>/', methods=["PUT"])
@jwt_required()
def edit_profile(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('pos.db') as conn:
            incoming_data = dict(request.json)
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

            if incoming_data.get('id_number') is not None:
                put_data['id_number'] = incoming_data.get('id_number')
                with sqlite3.connect('pos.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user SET id_number =? WHERE id=?", (put_data['id_number'], id))
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


@app.route('/add-product/', methods=["POST"])
@jwt_required()
def add_product():
    response = {}

    if request.method == "POST":
        product = request.form['product']
        category = request.form['category']
        description = request.form['description']
        dimensions = request.form['dimensions']
        price = request.form['price']
        id = request.form['id']

        with sqlite3.connect('pos.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (product, category, description, dimensions, price, id) "
                           "VALUES(?, ?, ?, ?, ?, ?)", (product, category, description, dimensions, price, id))
            conn.commit()
            response["status_code"] = 201
            response['description'] = "Product added successfully"
        return response


@app.route('/delete-product/<int:product_id>')
@jwt_required()
def delete_product(product_id):
    response = {}
    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product WHERE product_id=" + str(product_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"
    return response


@app.route('/edit-product/<int:product_id>/', methods=["PUT"])
@jwt_required()
def edit_product(product_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('pos.db') as conn:
            incoming_data = dict(request.json)
            put_data = {}

        if incoming_data.get('product') is not None:
            put_data['product'] = incoming_data.get('product')
            with sqlite3.connect('pos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET product =? WHERE product_id=?", (put_data['product'], product_id))
                conn.commit()
                response['status_code'] = 200
                response['message'] = "Product successfully updated."

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


@app.route('/get-products/', methods=["GET"])
@jwt_required()
def get_products():
    response = {}

    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = products
    return response


@app.route('/view-product/<int:product_id>', methods=["GET"])
def view_product(product_id):
    response = {}

    with sqlite3.connect('pos.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product WHERE product_id=" + str(product_id))

        response['status_code'] = 200
        response['description'] = "Product was successfully retrieved"
        response['data'] = cursor.fetchone()

    return jsonify(response)


if __name__ == '__main__':
    app.run()
