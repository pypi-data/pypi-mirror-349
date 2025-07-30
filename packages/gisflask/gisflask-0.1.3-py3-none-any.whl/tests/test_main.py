import unittest
import json
from app import create_app
from app.extensions import db
from app.models import User, Role, MapPreference

class MainTestCase(unittest.TestCase):
    """Test case for main functionality"""

    def setUp(self):
        """Setup test client and initialize app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        # Create application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Create a test user with token
        from app.extensions import bcrypt
        password_hash = bcrypt.generate_password_hash('test_password').decode('utf-8')
        self.test_user = User(
            username='test_user',
            email='test@example.com',
            password_hash=password_hash
        )
        
        # Create a default role
        test_role = Role(name='user', description='Regular user')
        
        db.session.add(test_role)
        db.session.commit()
        
        self.test_user.roles.append(test_role)
        db.session.add(self.test_user)
        db.session.commit()
        
        # Login to get token
        from flask_jwt_extended import create_access_token
        self.access_token = create_access_token(identity=self.test_user.id)

    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_map_route(self):
        """Test the map route"""
        response = self.client.get('/map')
        self.assertEqual(response.status_code, 200)
        
        # Test with parameters
        response = self.client.get('/map?map_type=folium&lat=51.5&lng=-0.1&zoom=10')
        self.assertEqual(response.status_code, 200)
        
    def test_health_check(self):
        """Test the health check route"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        
    def test_map_preferences(self):
        """Test the map preferences API"""
        # Get default preferences (no existing preferences)
        response = self.client.get(
            '/api/map/preferences',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['map_type'], 'folium')
        
        # Update preferences
        new_prefs = {
            'map_type': 'leafmap',
            'center_lat': 40.7128,
            'center_lng': -74.0060,
            'zoom_level': 10
        }
        
        response = self.client.post(
            '/api/map/preferences',
            json=new_prefs,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Check if preferences were updated
        response = self.client.get(
            '/api/map/preferences',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(data['map_type'], 'leafmap')
        self.assertEqual(data['center_lat'], 40.7128)
        self.assertEqual(data['center_lng'], -74.0060)
        self.assertEqual(data['zoom_level'], 10)
        
    def test_unauthenticated_map_preferences(self):
        """Test map preferences API without authentication"""
        response = self.client.get('/api/map/preferences')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
