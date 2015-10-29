import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG=True
SQLALCHEMY_DATABASE_URI="sqlite:///"+ BASE_DIR + "/app.db"
SQLALCHEMY_TRACK_MODIFICATIONS=True
UPLOAD_PATH = '/static/uploads/cover-images/'
UPLOAD_FOLDER = BASE_DIR + UPLOAD_PATH