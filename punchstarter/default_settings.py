import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = os.environ.get('DEBUG', True)
SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',"sqlite:///"+ BASE_DIR + "/app.db")
SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',True)
UPLOAD_PATH = '/static/uploads/cover-images/'
UPLOAD_FOLDER = BASE_DIR + UPLOAD_PATH