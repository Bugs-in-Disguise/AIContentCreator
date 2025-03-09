from wtforms import Form, StringField, BooleanField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# validators can have the form have specific requirements about lengths and stuff like that\

class LoginForm(Form):
    username = StringField('Name', [validators.length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [
        validators.DataRequired(), # make sure they include this
        validators.EqualTo('confirm', message="Passwords must match") # make sure this matches the confirm field
    ])
    confirm = PasswordField('Repeat Password')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
