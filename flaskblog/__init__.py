from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ed25e79e7d5c8e5fbf16f2a585e9c3cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

login_manager = LoginManager(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flaskblog import routes