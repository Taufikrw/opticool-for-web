from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from cryptography.fernet import Fernet

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
print(app.config["API_URL"])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
model = load_model(app.config["MODEL_FILE"])
class_names = ['Heart', 'Oval', 'Round', 'Square']
key = app.config["ENCRYPTION_KEY"]
cipher_suite = Fernet(key)

from app.routes import api, web, errors
from app.models import users, eyeglasses, encryptedfield