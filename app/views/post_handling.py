from app.forms import CreatePostForm
from app.models import Post, Image
from app.models import db
from flask import request, flash, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from flask_login import current_user

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
    if 'file' not in request.files:
        flash("No file", "danger")

    file = request.files.get('post_image')

    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(request.url)
    
    file_extension = allowed_file(file.filename)

    if file and file_extension in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)

        # read the file as binary
        image_data = file.read()

        return image_data, filename, file_extension
    else:
        flash("Invalid file type", "danger")
        return redirect(request.url)

def create_post():
    form = CreatePostForm(request.form)
    if request.method == "POST" and form.validate():
        title = request.form.get("title")
        description = request.form.get("description")

        new_post = Post(
            title=title,
            description=description,
            user_id=current_user.id
        )

        # upload the new post to the db
        db.session.add(new_post)
        db.session.commit()

        image = upload_image()

        new_image = Image(
            image=image[0],
            name=image[1],
            extension=image[2],
            post_id=new_post.id
        )

        db.session.add(new_image)
        db.session.commit()

        return redirect(next or url_for('main.default'))
    else:
        return render_template('posts/create_post.html', form=form) # give them the create post page and keep their form data if they're just being routed back to it

# this should ONLY
def serve_post(filename): 
    image = db.session.execute(db.Query(Image).filter_by(name=filename)).scalar_one_or_none()
    if image is not None:
        return send_file(BytesIO(image.image), mimetype=f"image/{image.extension}") # be aware that extensions are capitalized for some reason
    else:
        return redirect(url_for('main.default'))