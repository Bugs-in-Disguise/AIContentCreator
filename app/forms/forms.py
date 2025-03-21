from wtforms import Form, StringField, PasswordField, validators, FileField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed

# validators can have the form have specific requirements about lengths and stuff like that\

class LoginForm(Form):
    username = StringField('Name', [validators.length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    submit = SubmitField('Login')

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_type = StringField('Business Type', validators=[DataRequired(), Length(min=4, max=25)])
    insta_username = StringField('Instagram Email', validators=[DataRequired()])
    insta_password = PasswordField('Instagram Password', [validators.DataRequired()])
    password = PasswordField('ContentFlow Password', [
        validators.DataRequired(), # make sure they include this
        validators.EqualTo('confirm_password', message="Passwords must match") # make sure this matches the confirm field
    ])
    confirm_password = PasswordField('Confirm ContentFlow Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class CreatePostForm(Form):
    title = StringField('Title', [validators.length(min=1, max=20)]) # should research what good lengths are for titles
    description = StringField("Description", [validators.length(min=1)]) # should also do that resarch for descriptions
    post_image = FileField("Post's image", validators=[
        # FileRequired(), TODO: FIX THIS https://stackoverflow.com/questions/69114986/flask-wtforms-validation-fails-with-filerequired-validator-even-though-t
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!') 
    ])
    schedule_post = BooleanField("Schedule this post?")
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Post')
