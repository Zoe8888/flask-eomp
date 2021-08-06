import unittest
from app import app


class App(unittest.TestCase):
    def test_registration(self):
        test = app.test_client(self)
        response = test.get('/registration/')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_login(self):
        test = app.test_client(self)
        response = test.get('/login/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_display_users(self):
        test = app.test_client(self)
        response = test.get('/display-users/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_view_profile(self):
        test = app.test_client(self)
        response = test.get('/view-profile/<int:id>/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_edit_profile(self):
        test = app.test_client(self)
        response = test.get('/edit-profile/<int:id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    def test_delete_profile(self):
        test = app.test_client(self)
        response = test.get('/delete-profile/<int:id>/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_add_product(self):
        test = app.test_client(self)
        response = test.get('/add-product/')
        status = response.status_code
        self.assertEqual(status, 405)

    def test_edit_product(self):
        test = app.test_client(self)
        response = test.get('/edit-product/<int:product_id>/')
        status = response.status_code
        self.assertEqual(status, 404)

    def test_delete_product(self):
        test = app.test_client(self)
        response = test.get('/delete-product/<int:product_id>')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_show_products(self):
        test = app.test_client(self)
        response = test.get('/show-products/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_view_product(self):
        test = app.test_client(self)
        response = test.get('/view-product/<int:product_id>')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_view_users_product(self):
        test = app.test_client(self)
        response = test.get('/view_users-product/<int:product_id>')
        status = response.status_code
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()
