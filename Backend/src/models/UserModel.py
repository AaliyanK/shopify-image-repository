from marshmallow import fields, Schema
import datetime
from . import db
from . import bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.email = data['email']
        self.password = self.__generate_hash(data['password'])
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(value)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()
    
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all_users():
        return UserModel.query.all()
    
    @staticmethod
    def get_one_user(user_id):
        return UserModel.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    def __repr(self):
        return '<id {}>'.format(self.user_id)

class UserSchema(Schema):
  """
  User Schema
  """
  user_id = fields.Int(dump_only=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)