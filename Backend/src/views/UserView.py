from flask import request, json, Response, Blueprint, jsonify
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()

  # check if JSON format is correct
  if req_data is None \
      or 'email' not in req_data \
      or 'password' not in req_data:
    return jsonify({'message': 'Valid JSON properties required'}), 400

  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(req_data['email'])
  if user_in_db:
    message = {'error': 'User already exists, please supply another email address'}
    return jsonify({'message': message}), 400
  
  # Save user to database
  user = UserModel(req_data)
  user.save()

  ser_data = user_schema.dump(user)

  # Create JWT session token
  token = Auth.generate_token(ser_data['user_id'])

  return jsonify({
    'message': 'user registered successfully',
    'jwt_token': token}), 201

@user_api.route('/login', methods=['GET'])
def login():
  req_data = request.args

  # check if JSON format is correct
  if req_data is None \
      or req_data['email'] is '' \
      or req_data['password'] is '':
    return jsonify({'message': 'Valid JSON properties required'}), 400
  
  user = UserModel.get_user_by_email(req_data['email'])

  # Ensure user exists in DB
  if not user:
    return jsonify({'error': 'invalid login credentials'}), 401
  
  # Ensure password is correct
  if not user.check_hash(req_data['password']):
    return jsonify({'error': 'invalid credentials'}), 401
  
  ser_data = user_schema.dump(user)
  
  # Generate JWT token
  token = Auth.generate_token(ser_data['user_id'])

  return jsonify({'message': 'login successful',
  'jwt_token': token}), 200

