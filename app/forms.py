from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired,DataRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=50)
    ])
    phone = StringField('Phone', validators=[
        DataRequired(), Regexp(r'^\d+$', message="Phone must contain digits only")
    ])
    address = StringField('Address', validators=[
        DataRequired(), Length(max=500)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=5, max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Update Profile')