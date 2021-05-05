from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker

# initialize our db
db = SQLAlchemy()
Session = sessionmaker()
bcrypt = Bcrypt()