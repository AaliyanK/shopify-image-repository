import os
class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/image_repository'
    # AWS_ACCESS_KEY_ID = "AKIAV7B2RSW3D3GDS4PU"
    # AWS_SECRET_ACCESS_KEY = "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"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


app_config = {
    'development': Development,
}
