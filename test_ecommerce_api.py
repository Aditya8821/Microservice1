import unittest
from flask import json
from ecommerce_api import app

class TestEcommerceAPI(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    def test_add_product(self):
        # Test adding a product
        product_data = {
            "id": "123",
            "name": "TestProduct",
            "price": 9.99,
            "quantity": 100
        }

        response = self.app.post('/add', json=product_data)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Product added successfully')

if __name__ == '__main__':
    unittest.main()
