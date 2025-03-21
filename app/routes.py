from flask import Blueprint
from app.models import User, Post
from flask_login import LoginManager, login_required, current_user
from app.views import load_user, login, logout, register, serve_post, create_post, get_image, post_to_ig
from flask import render_template, request, flash, redirect, url_for
import calendar
from datetime import date, timedelta
main = Blueprint("main", __name__, template_folder="templates")
from app.models import db
from app.models import Image as ImageModel
from io import BytesIO

login_manager = LoginManager()

# example of using the rest api (this should be removed at some point, all endpoints should be made in the views folder
@main.route("/", methods=['GET'])
@login_required
def default():
    return render_template("about.html")

# About page route
@main.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@main.route("/calender", methods=['GET'])
@login_required
def calender():
    # Get the current month and year from query parameters (default to the current month)
    year = request.args.get('year', type=int, default=date.today().year)
    month = request.args.get('month', type=int, default=date.today().month)

    # Get all posts for the current user
    user_posts = Post.query.filter_by(user_id=current_user.id).all()

    # Generate the start and end dates for the selected month
    start_date = date(year, month, 1)
    _, days_in_month = calendar.monthrange(year, month)
    end_date = date(year, month, days_in_month)

    # Get the weekday of the first day of the month
    first_weekday = start_date.weekday()  # 0 = Monday, 6 = Sunday

    calendar_days = []
    # Add empty days for alignment
    for _ in range(first_weekday):
        calendar_days.append({'date': None, 'posts': []})

    # Add actual days
    current_date = start_date
    while current_date <= end_date:
        day_posts = [post for post in user_posts if post.date == current_date]
        calendar_days.append({'date': current_date, 'posts': day_posts})
        current_date += timedelta(days=1)

    # Calculate the previous and next months
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template(
        'calender.html',
        calendar_days=calendar_days,
        current_month=month,
        current_year=year,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year
    )

@main.route('/post_to_instagram/<int:post_id>', methods=['POST'])
@login_required
def post_to_instagram(post_id):
    # Fetch the post and its associated image
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar_one_or_none()
    image = db.session.execute(db.select(ImageModel).filter_by(post_id=post_id)).scalar_one_or_none()

    if not post or not image:
        flash("Post or image not found", "danger")
        return redirect(url_for('main.serve_post', title=post.title))

    # Get the Instagram password from the form
    insta_password = request.form.get("insta_password")
    if not insta_password:
        flash("Instagram password is required to post.", "danger")
        return redirect(url_for('main.serve_post', title=post.title))

    # Call the post_to_ig function
    try:
        post_to_ig(BytesIO(image.image), post.description, insta_password)
        flash("Post successfully uploaded to Instagram!", "success")
    except Exception as e:
        flash(f"Failed to post to Instagram: {str(e)}", "danger")

    return redirect(url_for('main.serve_post', title=post.title))



# set the user loader callback (the function to return a user object given an id)
login_manager.user_loader(load_user)
login_manager.login_view = "main.login"

# add the login url
main.add_url_rule("/login", view_func=login, methods=['GET', 'POST'])

# add main logout url
main.add_url_rule("/logout", view_func=logout, methods=['GET'])
# login_required(logout)

main.add_url_rule("/register", view_func=register, methods=["GET", "POST"])

main.add_url_rule("/create_post", view_func=login_required(create_post), methods=["GET", "POST"])

main.add_url_rule("/post/<string:title>", view_func=login_required(serve_post), methods=["GET", "POST"])

main.add_url_rule("/image/<int:post_id>", view_func=login_required(get_image), methods=["GET"])
