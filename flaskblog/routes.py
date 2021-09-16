from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


# dummy data
posts = [
    {
        "author": "John Williams",
        "title": "Blog Post One",
        "content": "Conentent of the Post One",
        "date": 2021
    },
    {
        "author": "Joe Hisaishi",
        "title": "Blog Post Two",
        "content": "Conentent of the Post Two",
        "date": 2021 
    }
]


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
