from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# note about db.relationship() vs db.Column(db.ForeignKey):
# You'll always need to make a foreign key column to establish a relationship
# However, you should add a db.relationship in the 'Parent' model, so that we can use ORM functionality to point to the 'child' models
# Also, I'm using the 'backref' option instead of the 'back_populates' for relationships because it automatically handles establishing the bi-direction relationship
# uselist=False makes it a one-to-one relationship, but the relationship() function establishes a one-to-many relationship by default if 'uselist' isn't specified

# need expierence, and this will be given an update to us from the fontend
class User(UserMixin, db.Model): # needs to inherit from UserMixin to be compatible with flask-login
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    email = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)