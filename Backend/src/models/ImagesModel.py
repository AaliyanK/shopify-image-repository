from marshmallow import fields, Schema
import datetime
from . import db

class ImagesModel(db.Model):
    __tablename__ = 'images'

    image_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.image_url = data.get('image_url')
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all_images():
        return ImagesModel.query.all()
    
    @staticmethod
    def get_one_image(image_id):
        return ImagesModel.query.filter_by(image_id=image_id).first()
    
    @staticmethod
    def get_images_by_user_id(user_id):
        return ImagesModel.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def delete_image(image_id):
        ImagesModel.query.filter_by(image_id=image_id).first().delete()
        db.session.commit()
    def __repr(self):
        return '<id {}>'.format(self.image_id)

class ImagesSchema(Schema):
  """
  Images Schema
  """
  image_id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  image_url = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)