from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ed25e79e7d5c8e5fbf16f2a585e9c3cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# export to models.py
login_manager = LoginManager(app)
# redirects to .../login if @login_required  
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flaskblog import routes
