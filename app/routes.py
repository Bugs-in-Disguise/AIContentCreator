from flask import Blueprint
from app.models import User
main = Blueprint("main", __name__)

# example of using the rest api (this should be removed at some point, all endpoints should be made in the views folder
@main.route("/", methods=['GET'])
def default():
    return "<p> Hello World! </p>"
