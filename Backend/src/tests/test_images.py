import unittest
import os
import json
import boto3
from ..app import create_app, db

class ImagesTest(unittest.TestCase):
  """
  Images Test Case
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
    self.data = {
        'data': 'data'
    }

    with self.app.app_context():
        # create all tables
        db.create_all()
    
    def test_image_upload(self):
        """ test image upload with valid credentials"""
        res = self.client().post('/api/v1/images/upload', headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        json_data = json.loads(res.data)
        s3_client = boto3.client('s3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
        s3_client.upload_fileobj(data,'test_bucket',data['data'])
        self.assertEqual(res.status_code, 201)

    def test_image_delete(self):
        """ test image delete with valid credentials"""
        res = self.client().post('/api/v1/images/delete/<image_id>', headers={'Content-Type': 'application/json'}, data=json.dumps(self.data))
        json_data = json.loads(res.data)
        s3_client = boto3.client('s3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
        s3_client.delete_fileobj(data,'test_bucket',data['data'])
        self.assertEqual(res.status_code, 201)
        
if __name__ == "__main__":
  unittest.main() 