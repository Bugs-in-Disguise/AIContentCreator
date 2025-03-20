from flask import Blueprint
from app.models import User
from app.views import load_user, login, logout, register, serve_post, create_post, get_image
from flask_login import LoginManager, login_required
from flask import render_template
import calendar
main = Blueprint("main", __name__, template_folder="templates")

login_manager = LoginManager()

# example of using the rest api (this should be removed at some point, all endpoints should be made in the views folder
@main.route("/", methods=['GET'])
@login_required
def default():
    return render_template("home/index.html")

# About page route
@main.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@main.route("/calender", methods=['GET'])
@login_required
def calender():
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    return render_template('calender.html', calendar=cal.formatmonth(2025, 4))
    

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

main.add_url_rule("/post/<string:title>", view_func=serve_post, methods=["GET", "POST"])
# login_required(serve_post)

main.add_url_rule("/image/<int:post_id>", view_func=get_image, methods=["GET"])