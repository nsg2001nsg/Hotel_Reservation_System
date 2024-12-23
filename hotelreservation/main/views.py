from flask import render_template, request, Blueprint

from hotelreservation.models import Hotel

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    return render_template("hello.html", title="Hello", block_title="Hello Page")


@main.route("/home/", methods=["GET", "POST"])
def home():
    print(f"request.method: {request.method}")
    hotel_name = request.form["Names"]
    hotel_citi = request.form["Cities"]
    hotel_state = request.form["States"]
    # if request.method == "POST":
    #     pass

    page = request.args.get("page", 1, type=int)
    hotels = Hotel.query.order_by(Hotel.date_posted.desc()).paginate(page=page, per_page=5)
    hotel_names = Hotel.query.group_by(Hotel.name).order_by(Hotel.name.asc()).distinct().values(Hotel.name)
    hotel_names = [i[0] for i in hotel_names]
    hotel_cities = Hotel.query.group_by(Hotel.city).order_by(Hotel.city.asc()).distinct().values(Hotel.city)
    hotel_cities = [i[0] for i in hotel_cities]
    hotel_states = Hotel.query.group_by(Hotel.state).order_by(Hotel.state.asc()).distinct().values(Hotel.state)
    hotel_states = [i[0] for i in hotel_states]
    return render_template("home.html", title="Home", block_title="Home Page", hotels=hotels,
                           hotel_names=hotel_names, hotel_cities=hotel_cities, hotel_states=hotel_states)


@main.route("/about/")
def about():
    return render_template("about.html", title="About", block_title="About Page")
