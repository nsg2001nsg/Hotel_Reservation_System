from flask import render_template, request, Blueprint

from hotelreservation.models import Hotel

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    return render_template("hello.html", title="Hello", block_title="Hello Page")


@main.route("/home/")
def home():
    page = request.args.get("page", 1, type=int)
    hotels = Hotel.query.order_by(Hotel.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", title="Home", block_title="Home Page", hotels=hotels)


@main.route("/about/")
def about():
    return render_template("about.html", title="About", block_title="About Page")
