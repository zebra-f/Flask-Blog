import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home')
@app.route('/')
def index():

    posts = Post.query.all()

    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    # redirects to the homepage if we're already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    # POST method
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

    form = LoginForm()

    # POST method 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # redirects to the hompage if the login process was successful
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            # http://127.0.0.1:5000/login?next=%2Faccount next_page = account or None 
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Wrong email or password, please try again', 'danger')
            
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension

    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_filename)

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    
    image.save(picture_path)

    return picture_filename


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    
    form = UpdateAccountForm()
    
    # POST method
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    
    # GET method
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', 
                        filename='profile_pictures/' + current_user.image_file)
    
    return render_template('account.html', 
                        title='Your Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():

        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Post has been created', 'success')
        return redirect(url_for('index'))


    return render_template('new_post.html', 
                        title='New Post', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)