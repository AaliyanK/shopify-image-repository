from flask import request, json, Response, Blueprint, jsonify
from flask import current_app as app
from ..models.ImagesModel import ImagesModel, ImagesSchema
from ..shared.Authentication import Auth
import boto3

images_api = Blueprint('images', __name__)
images_schema = ImagesSchema()
BUCKET = 'shopify-image-storage'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

# To upload image to S3 and add to Database
@images_api.route('/upload', methods=['POST'])
@Auth.auth_required
def image_upload(current_user):
    image_data = request.files['file']
    filename = image_data.filename

    # check if JSON format is correct
    if image_data is None:
        return jsonify({'message': 'Valid JSON properties required'}), 400
    
    # check if the file extension is valid
    if not "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        return jsonify({'message': 'Valid file extension required'}), 400
    
    # Init AWS S3 client
    s3_client = boto3.client('s3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    
    # Upload to S3, note that the bucket link is public
    s3_client.upload_fileobj(image_data,BUCKET,filename)
    save_to_db = {'user_id':current_user['id'],"image_url":f'https://{BUCKET}.s3.us-east-2.amazonaws.com/{filename}'}

    # Save entries to DB
    images = ImagesModel(save_to_db)
    images.save()

    return jsonify({'message':'Image added to S3 and DB'})

# Get request will populate homepage with images from S3
@images_api.route('/view', methods=['GET'])
@Auth.auth_required
def image_view(current_user):
    image_list = ImagesModel.get_images_by_user_id(current_user['id'])
    image_data = []
    
    for images in image_list:
        image_dict = {}
        image_dict['image_id'] = images.image_id
        image_dict['image_url'] = images.image_url
        image_data.append(image_dict)
    
    return jsonify(image_data), 200

@images_api.route('/delete/<image_id>', methods=['DELETE'])
@Auth.auth_required
def image_delete(current_user,image_id):
    req = request.get_json()
    
    # Delete from S3
    # Init AWS S3 client
    s3_client = boto3.client('s3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

    # Delete from DB
    ImagesModel.delete_image(image_id)
    
    # Delete from S3
    url = req['image_url'].split('/')[-1]
    s3_client.delete_object(Bucket=BUCKET, Key=url)
    
    return jsonify({'message':'deleted successfuly'}), 200