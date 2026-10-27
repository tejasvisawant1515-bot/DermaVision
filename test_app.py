"""
Automated Integration and Functional Test Suite for DermaVisionAI
Verifies all routes, database operations, AI scanning, and budget updates.
"""

import os
import unittest
from app import app
from database import db_manager

class DermaVisionAITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DermaVision', response.data)
        self.assertIn(b'Start Free Skin Scan', response.data)

    def test_02_analyze_page(self):
        response = self.client.get('/analyze')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live Camera', response.data)
        self.assertIn(b'Upload Photo', response.data)
        self.assertIn(b'Select Your Skincare Budget', response.data)

    def test_03_user_registration_and_login(self):
        # Register test user
        uname = 'testuser_' + os.urandom(3).hex()
        email = f"{uname}@example.com"
        reg_res = self.client.post('/register', data={
            'username': uname,
            'email': email,
            'full_name': 'Test User',
            'password': 'password123',
            'confirm_password': 'password123',
            'age': 25,
            'gender': 'Female'
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b'Welcome to DermaVisionAI', reg_res.data)

        # Logout
        self.client.get('/logout', follow_redirects=True)

        # Login
        login_res = self.client.post('/login', data={
            'login_input': uname,
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Welcome back', login_res.data)

    def test_04_full_skin_scan_flow(self):
        sample_img = os.path.join(app.root_path, 'static', 'samples', 'sample_combination_acne.jpg')
        self.assertTrue(os.path.exists(sample_img), f"Sample image missing at {sample_img}")

        with open(sample_img, 'rb') as f:
            res = self.client.post('/analyze', data={
                'image_file': (f, 'test_face.jpg'),
                'budget': '1200'
            }, content_type='multipart/form-data', follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        # Should render results page
        self.assertIn(b'Personalized Dermatological Analysis', res.data)
        self.assertIn(b'Identified Skin Type', res.data)
        self.assertIn(b'Recommended Skincare Products', res.data)
        self.assertIn(b'Morning (AM) Routine', res.data)
        self.assertIn(b'Night (PM) Routine', res.data)

    def test_05_dynamic_budget_api(self):
        # Retrieve recent analysis
        conn, engine = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM analysis_history ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            analysis_id = row[0] if isinstance(row, tuple) else row['id']
            # Test updating budget to 2500
            res = self.client.post(f'/api/update_budget/{analysis_id}', json={'budget': 2500})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])
            self.assertGreater(len(data['products']), 0)
            self.assertIn('morning', data['routine'])
            self.assertIn('night', data['routine'])

    def test_06_products_catalog_page(self):
        res = self.client.get('/products?skin_type=Oily&category=Cleanser')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Cleanser', res.data)

    def test_07_about_page(self):
        res = self.client.get('/about')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Technology Stack', res.data)
        self.assertIn(b'Medical Disclaimer', res.data)

    def test_08_cart_management(self):
        # Test adding product to cart
        add_res = self.client.post('/api/cart/add', json={
            'product_id': 1,
            'quantity': 2
        })
        self.assertEqual(add_res.status_code, 200)
        data = add_res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['cart_count'], 2)

        # View cart
        cart_view = self.client.get('/cart')
        self.assertEqual(cart_view.status_code, 200)
        self.assertIn(b'Your Skincare Cart', cart_view.data)

    def test_09_checkout_and_order_placement(self):
        # Ensure cart has items
        self.client.post('/api/cart/add', json={'product_id': 1, 'quantity': 1})

        # View checkout page
        checkout_page = self.client.get('/checkout')
        self.assertEqual(checkout_page.status_code, 200)
        self.assertIn(b'Secure Checkout', checkout_page.data)

        # Submit checkout order
        order_post = self.client.post('/checkout/process', data={
            'full_name': 'Aarav Patel',
            'phone': '9876543210',
            'address_line1': '101 Lotus Residency, Indiranagar',
            'address_line2': 'Near 100 Feet Road',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pincode': '560038',
            'payment_method': 'UPI',
            'shipping_speed': 'standard'
        }, follow_redirects=True)

        self.assertEqual(order_post.status_code, 200)
        self.assertIn(b'Your Order is Confirmed', order_post.data)
        self.assertIn(b'Aarav Patel', order_post.data)
        self.assertIn(b'Purchased Skincare Items', order_post.data)

    def test_10_authenticated_order_and_history(self):
        # Register and log in a user
        uname = 'authuser_' + os.urandom(3).hex()
        email = f"{uname}@example.com"
        self.client.post('/register', data={
            'username': uname,
            'email': email,
            'full_name': 'Ananya Sen',
            'password': 'password123',
            'confirm_password': 'password123',
            'age': 28,
            'gender': 'Female'
        }, follow_redirects=True)

        # Add to cart
        self.client.post('/api/cart/add', json={'product_id': 2, 'quantity': 1})

        # Process checkout with address saving
        res = self.client.post('/checkout/process', data={
            'full_name': 'Ananya Sen',
            'phone': '9811223344',
            'address_line1': 'Flat 204, Green Meadows',
            'address_line2': 'Koramangala 4th Block',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pincode': '560034',
            'payment_method': 'Credit/Debit Card',
            'shipping_speed': 'standard',
            'save_address': '1'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Your Order is Confirmed', res.data)

        # Check orders list
        orders_res = self.client.get('/orders')
        self.assertEqual(orders_res.status_code, 200)
        self.assertIn(b'Ananya Sen', orders_res.data)

        # Check profile page
        profile_res = self.client.get('/profile')
        self.assertEqual(profile_res.status_code, 200)
        self.assertIn(b'Ananya Sen', profile_res.data)

if __name__ == '__main__':
    unittest.main()
