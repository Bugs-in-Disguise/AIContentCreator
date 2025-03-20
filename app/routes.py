from flask import Blueprint
from app.models import User, Post
from flask_login import LoginManager, login_required, current_user
from app.views import load_user, login, logout, register, serve_post, create_post, get_image
from flask import render_template
# import calendar
from datetime import date, timedelta
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
    # Get all posts for the current user (assuming user is logged in)
    user_posts = Post.query.filter_by(user_id=current_user.id).all()  # current_user is now defined

    # Generate a list of days for the current month
    today = date.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)

    calendar_days = []
    current_date = start_date
    while current_date <= end_date:
        # Filter posts for the current day
        day_posts = [post for post in user_posts if post.date == current_date]
        calendar_days.append({'date': current_date, 'posts': day_posts})
        current_date += timedelta(days=1)

    return render_template('calendar.html', calendar_days=calendar_days)

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
