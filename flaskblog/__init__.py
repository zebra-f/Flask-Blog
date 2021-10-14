from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ed25e79e7d5c8e5fbf16f2a585e9c3cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# export to models.py
login_manager = LoginManager(app)
# redirects to .../login if @login_required  
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# mail settings
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_POR'] = 587
app.config['MAIL_USER_TLS'] = True
# config file
app.config['MAIL_USERNAME'] = placeholder_1 = 1  # username placeholder
app.config['MAIL_PASSWORD'] = placeholder_2 = 2  # password placeholder  

mail = Mail(app)

# export to models.py
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flaskblog import routes
