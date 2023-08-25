import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_register(self):
        response = self.app.post('/register', data=dict(username='testuser', password='testpassword'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'User registered successfully')

    def test_login(self):
        response = self.app.post('/login', data=dict(username='testuser', password='testpassword'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Login successful')

    def test_account(self):
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 200)
        # Add assertions to verify the account information

if name == 'main':
    unittest.main()