# pip install flask-wtf
# pip install wtforms[email]
from re import sub
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # checks if the username is already taken 
    def validate_username(self, username):   
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken, choose a different one')

    # checks if the email is already taken 
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already taken, choose a different one')
        

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Change your Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


    # checks if the username is already taken 
    def validate_username(self, username):   
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken, choose a different one')

    # checks if the email is already taken 
    def validate_email(self, email):
        if email.data != current_user.email:    
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is already taken, choose a different one')

    
class PostForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                        validators=[DataRequired()])
    
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    # checks if the email is already taken
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')