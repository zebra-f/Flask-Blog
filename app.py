from enum import unique
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import backref
from forms import RegistrationForm, LoginForm
from datetime import datetime

def current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# dummy data
posts = [
    {
        "author": "John Williams",
        "title": "Blog Post One",
        "content": "Conentent of the Post One",
        "date": current_datetime()
    },
    {
        "author": "Joe Hisaishi",
        "title": "Blog Post Two",
        "content": "Conentent of the Post Two",
        "date": current_datetime() 
    }
]


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ed25e79e7d5c8e5fbf16f2a585e9c3cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm() 
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '1234':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Unsuccessful', 'danger')
            
    return render_template('login.html', title='Register', form=form)




if __name__ == '__main__':
    app.run(debug=True)