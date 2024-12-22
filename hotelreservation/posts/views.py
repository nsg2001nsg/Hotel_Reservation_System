from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from hotelreservation import db
from hotelreservation.posts.forms import PostForm
from hotelreservation.models import Post

posts = Blueprint("posts", __name__)


@posts.route("/posts/create/", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your posts has been created.", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="Create Post", block_title="Create Post Page",
                           legend="Create Post Info", form=form)


@posts.route("/posts/<int:post_id>/")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, block_title="Post Page", post=post)


@posts.route("/posts/<int:post_id>/update/", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your posts has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", block_title="Update Post Page",
                           legend="Update Post Info", form=form)


@posts.route("/posts/<int:post_id>/delete/", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your posts has been deleted.", "success")
    return redirect(url_for("main.home"))
