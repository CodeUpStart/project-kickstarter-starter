import os 
import cloudinary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = os.environ.get('DEBUG', True)
SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',"sqlite:///"+ BASE_DIR + "/app.db")
SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',True)
CLOUDINARY_CLOUD_NAME=os.environ.get('CLOUDINARY_CLOUD_NAME',"dg9i8jwk4")
CLOUDINARY_API_KEY=os.environ.get('CLOUDINARY_API_KEY',"643998768374314")
CLOUDINARY_API_SECRET=os.environ.get('CLOUDINARY_API_SECRET',"NPmM03goRfAXz3duedckDwn5_qQ")

cloudinary.config( 
  cloud_name = CLOUDINARY_CLOUD_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET 
)