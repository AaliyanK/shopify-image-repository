import unittest
import os
import json
from ..app import create_app, db

class UsersTest(unittest.TestCase):
  """
  Users Test Case
  """
  def setUp(self):
    """
    Test Setup
    """
    self.app = create_app("development")
    self.client = self.app.test_client
    self.user = {
      'email': 'aaliyan@mail.com',
      'password': 'test'
    }

    with self.app.app_context():
        # create all tables
        db.create_all()
        
    def test_user_creation(self):
        """ test user creation with valid credentials """
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)
    
    def test_user_creation_with_no_password(self):
      """ test user creation with no password"""
      user1 = {
        'email': 'aaliyan@mail.com',
      }
      res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
      json_data = json.loads(res.data)
      self.assertEqual(res.status_code, 400)
      self.assertTrue(json_data.get('password'))
    
    def test_user_already_exists(self):
      """ test user creation with pre-created user"""
      user1 = {
        'email': 'aaliyan@mail.com',
        'password': 'test'
      }
      res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
      self.assertEqual(res.status_code,201)
      res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
      json_data = json.loads(res.data)
      self.assertEqual(json_data.get('error'), 'User already exists!')
      self.assertEqual(res.status_code, 400)

    def test_user_login(self):
      """ User Login Tests """
      res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
      self.assertEqual(res.status_code, 201)
      res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
      json_data = json.loads(res.data)
      self.assertTrue(json_data.get('jwt_token'))
      self.assertEqual(res.status_code, 200)
    
    def test_user_login_with_invalid_password(self):
      """ User Login Tests with invalid credentials """
      user1 = {
        'password': 'password',
        'email': 'aaliyan@mail.com',
      }
      res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
      self.assertEqual(res.status_code, 201)
      res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
      json_data = json.loads(res.data)
      self.assertFalse(json_data.get('jwt_token'))
      self.assertEqual(json_data.get('error'), 'invalid credentials')
      self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
  unittest.main() 