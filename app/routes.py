from flask import Blueprint
from app.models import User
from app.views import load_user, login, logout, register, serve_image, create_post
from flask_login import LoginManager, login_required
from flask import render_template
main = Blueprint("main", __name__, template_folder="templates")

login_manager = LoginManager()

# example of using the rest api (this should be removed at some point, all endpoints should be made in the views folder
@main.route("/", methods=['GET'])
@login_required
def default():
    return render_template("home/index.html")

# set the user loader callback (the function to return a user object given an id)
login_manager.user_loader(load_user)
login_manager.login_view = "main.login"

# add the login url
main.add_url_rule("/login", view_func=login, methods=['GET', 'POST'])

# add main logout url
main.add_url_rule("/logout", view_func=logout, methods=['GET'])
# login_required(logout)

main.add_url_rule("/register", view_func=register, methods=["GET", "POST"])

main.add_url_rule("/create_post", view_func=create_post, methods=["GET", "POST"])

main.add_url_rule("/image/<string:filename>", view_func=serve_image, methods=["GET"])
