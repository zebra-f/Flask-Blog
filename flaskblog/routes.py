from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    
    # redirects to the homepage if we're already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # POST method
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(username=form.username.data,
                    email= form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created, you\'re now able to sign in!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # redirects to the homepage if we're already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # POST method
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # redirects to the hompage if the login process was successful
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            # http://127.0.0.1:5000/login?next=%2Faccount next_page = aacount or None 
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Wrong email or password, please try again', 'danger')
            
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Your Account')