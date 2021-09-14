from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from forms import RegistrationForm, LoginForm


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