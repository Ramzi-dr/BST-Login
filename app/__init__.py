import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from datetime import timedelta




app = Flask(__name__)
app.config['SECRET_KEY'] = '876fec2a8b6e6768915bc941ddd58d8d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bst.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] =  os.environ.get('EMAIL_USER')#'bst.einbruchschutz@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
mail = Mail(app)
from app import routes


