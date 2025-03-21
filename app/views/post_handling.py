from app.forms import CreatePostForm
from app.models import Post
from app.models import Image as ImageModel
from app.models import db
from flask import request, flash, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from flask_login import current_user
from io import BytesIO
from InstaPost.captionGen import generate_instagram_post
from InstaPost.instaPost import *
import tempfile




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Specify allowed image types

def allowed_file(filename):
    is_valid_filename = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if is_valid_filename:
        file_extension = filename.rsplit('.', 1)[1].lower()
        file_extension =  "jpeg" if file_extension == 'jpg' else file_extension # make sure to have it be the right name for mimetype
        return file_extension
    else:
        return None

# i want this to just return the binary data for the image
def upload_image():
    if 'post_image' not in request.files:
        flash("No file", "danger")
        return None  # <-- Fix here

    file = request.files.get('post_image')

    if file.filename == '':
        flash("No selected file", "danger")
        return None  # <-- Fix here
    
    file_extension = allowed_file(file.filename)

    if file and file_extension in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)

        # read the file as binary
        image_data = file.read()

        return image_data, filename, file_extension
    else:
        flash("Invalid file type", "danger")
        return None  # <-- Fix here


def create_post():
    form = CreatePostForm(request.form)
    if request.method == "POST" and form.validate():
        title = request.form.get("title")
        description = request.form.get("description")
        post_date = request.form.get("date")
        scheduled = request.form.get("schedule_post")
        if scheduled == None:
            scheduled = False
        else:
            scheduled = True

        # generate the caption
        industry = current_user.business_type
        audience = "general"
        caption = generate_instagram_post(industry, audience, description)
        description = caption

        new_post = Post(
            title=title,
            description=description,
            user_id=current_user.id,
            date=post_date,
            scheduled=scheduled
        )

        # upload the new post to the db
        db.session.add(new_post)
        db.session.commit()

        image = upload_image()

        new_image = ImageModel(
            image=image[0],
            name=image[1],
            extension=image[2],
            post_id=new_post.id
        )

        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('main.serve_post', title=title))
    else:
        return render_template('posts/create_post.html', form=form) # give them the create post page and keep their form data if they're just being routed back to it

def serve_post(title):
    post = db.session.execute(db.select(Post).filter_by(title=title)).scalar_one_or_none()
    
    if request.method == 'POST':
        form = CreatePostForm(request.form)
        if form.validate():
            post.title = form.title.data
            post.description = form.description.data
            post.scheduled = form.schedule_post.data
            
            # Handle image upload
            image = upload_image()
            if image:
                existing_image = db.session.execute(db.select(ImageModel).filter_by(post_id=post.id)).scalar_one_or_none()
                if existing_image:
                    existing_image.image = image[0]
                    existing_image.name = image[1]
                    existing_image.extension = image[2]
                else:
                    new_image = ImageModel(
                        image=image[0],
                        name=image[1],
                        extension=image[2],
                        post_id=post.id
                    )
                    db.session.add(new_image)

            db.session.commit()
            return redirect(url_for('main.serve_post', title=post.title))
    else:
        form = CreatePostForm(obj=post)
        if post.scheduled == True:
            form.schedule_post.data = "y"
        # don't need an else because it'll just be unchecked by default

        # If an image exists, show it in the template
        existing_image = db.session.execute(db.select(ImageModel).filter_by(post_id=post.id)).scalar_one_or_none()
        if existing_image:
            image_url = url_for('main.get_image', post_id=post.id)
        else:
            image_url = None
    return render_template('posts/post.html', form=form, image_url=image_url, post=post)

def get_image(post_id):
    image = db.session.execute(db.select(ImageModel).filter_by(post_id=post_id)).scalar_one_or_none()
    if image:
        return send_file(BytesIO(image.image), mimetype=f'image/{image.extension}')
    else:
        flash("ImageModel not found", "danger")
        return redirect(url_for('main.default'))

def post_to_ig(picture, caption, password):
    # Log in to Instagram
    api = API(current_user.insta_username, password)
    api.login()
    if not api.is_logged_in:
        raise Exception("Failed to log in to Instagram")

    # Save the BytesIO object to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(picture.read())  # Write the binary data to the temp file
        temp_file_path = temp_file.name  # Get the path of the temp file

    # Upload the photo using the temporary file path
    try:
        api.upload_photo(temp_file_path, caption)
    finally:
        # Clean up the temporary file
        import os
        os.remove(temp_file_path)