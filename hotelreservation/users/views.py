from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from hotelreservation import db, bcrypt
from hotelreservation.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from hotelreservation.models import User, Post, Reservation
from hotelreservation.users.utils import save_picture, send_reset_email, send_registration_email

users = Blueprint("users", __name__)


@users.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created. You can login now.", "success")
        send_registration_email(user)
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", block_title="Register Page", legend="Register Info", form=form)


@users.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Login successful. Welcome {form.email.data}.", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", block_title="Login Page", legend="Login Info", form=form)


@users.route("/logout/")
def logout():
    logout_user()
    flash(f"Logout successful. You can login again.", "success")
    return redirect(url_for("users.login"))


@users.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", block_title="Account Page", legend="Account Info", image_file=image_file, form=form)


@users.route("/user/posts/<string:username>/")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", title="User Posts", block_title="User Posts Page", posts=posts, user=user)


@users.route("/user/reservations/<string:username>/")
def user_reservations(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    reservations = Reservation.query.filter_by(customer=user).order_by(Reservation.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_reservations.html", title="User Reservations", block_title="User Reservations Page", reservations=reservations, user=user)


@users.route("/reset_password/", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your registered email address with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", block_title="Reset Password Page", legend="Reset Password Info", form=form)


@users.route("/reset_password/<token>/", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("This is an invalid or expired token.", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated. You can login now.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", block_title="Reset Password Page", legend="Reset Password Info", form=form)
