import unittest
import json
from app import create_app
from app.extensions import db
from app.models import User, Role

class AuthTestCase(unittest.TestCase):
    """Test case for authentication functionality"""

    def setUp(self):
        """Setup test client and initialize app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        # Create application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Create a test user
        from app.extensions import bcrypt
        password_hash = bcrypt.generate_password_hash('test_password').decode('utf-8')
        test_user = User(
            username='test_user',
            email='test@example.com',
            password_hash=password_hash
        )
        
        # Create a default role
        test_role = Role(name='user', description='Regular user')
        
        db.session.add(test_role)
        db.session.commit()
        
        test_user.roles.append(test_role)
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        """Test user registration"""
        # Register a new user
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'new_user',
                'email': 'new_user@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User registered successfully')
        
        # Verify user was created in the database
        user = User.query.filter_by(username='new_user').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new_user@example.com')

    def test_login_user(self):
        """Test user login"""
        # Login with test user
        response = self.client.post(
            '/auth/login',
            json={
                'username': 'test_user',
                'password': 'test_password'
            },
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        # Login with incorrect password
        response = self.client.post(
            '/auth/login',
            json={
                'username': 'test_user',
                'password': 'wrong_password'
            },
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 401)
        
    def test_protected_route(self):
        """Test protected route access with and without token"""
        # Login to get token
        login_response = self.client.post(
            '/auth/login',
            json={
                'username': 'test_user',
                'password': 'test_password'
            },
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['access_token']
        
        # Access protected route without token
        response = self.client.get('/auth/protected')
        self.assertEqual(response.status_code, 401)
        
        # Access protected route with token
        response = self.client.get(
            '/auth/protected',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['logged_in_as'], 'test_user')

if __name__ == '__main__':
    unittest.main()
