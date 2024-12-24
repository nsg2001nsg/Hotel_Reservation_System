from flask import render_template, request, Blueprint

from hotelreservation.models import Hotel, Room

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    filters = {}
    hotels = Hotel.query.filter_by(**filters).order_by(Hotel.date_posted.desc())
    rooms = Room.query.filter_by(**filters).order_by(Room.date_posted.desc())
    return render_template("hello.html", title="Hello", block_title="Hello Page", hotels=hotels, rooms=rooms)


@main.route("/home/", methods=["GET", "POST"])
def home():
    page = request.args.get("page", 1, type=int)
    filter_key = request.args.get("filter_key", "", type=str)
    filter_val = request.args.get("filter_val", "", type=str)
    # print(f"request.args: {request.args}")
    print(f"request.form: {request.form}")
    select_name = request.form.getlist("name")
    len_name = len(select_name)
    select_city = request.form.getlist("city")
    len_city = len(select_city)
    select_state = request.form.getlist("state")
    len_state = len(select_state)
    print(f"request.form: ")
    if request.method == "POST":
        filter_dict = {
            "default": {},
            "name": {"name": request.form.get("name", "")},
            "city": {"city": request.form.get("city", "")},
            "state": {"state": request.form.get("state", "")},
        }
        filters = filter_dict.get(request.form.get("Filter", "default"))
        filter_key = request.form.get("Filter", "default")
        filter_val = filters.get(filter_key, "") if filters else filter_val
        print(f"filters: {filters}")
    else:
        filters = {}
    #     if request.form.get("Name", ""):
    #         hotel_name = request.form.get("Name", "")
    #         filters = {"name": hotel_name}
    #     elif request.form.get("City", ""):
    #         hotel_city = request.form.get("City", "")
    #         filters = {"city": hotel_city}
    #     elif request.form.get("State", ""):
    #         hotel_state = request.form.get("State", "")
    #         filters = {"state": hotel_state}
    # else:
    #     if hotel_name:
    #         filters = {"name": hotel_name}
    #     elif hotel_city:
    #         filters = {"city": hotel_city}
    #     elif hotel_state:
    #         filters = {"state": hotel_state}
    # filters = {}
    hotels = Hotel.query.filter_by(**filters).order_by(Hotel.date_posted.desc()).paginate(page=page, per_page=5)
    hotel_names = Hotel.query.group_by(Hotel.name).order_by(Hotel.name.asc()).distinct().values(Hotel.name)
    hotel_names = [i[0] for i in hotel_names]
    hotel_names.insert(0, "")
    hotel_cities = Hotel.query.group_by(Hotel.city).order_by(Hotel.city.asc()).distinct().values(Hotel.city)
    hotel_cities = [i[0] for i in hotel_cities]
    hotel_cities.insert(0, "")
    hotel_states = Hotel.query.group_by(Hotel.state).order_by(Hotel.state.asc()).distinct().values(Hotel.state)
    hotel_states = [i[0] for i in hotel_states]
    hotel_states.insert(0, "")
    return render_template("home.html", title="Home", block_title="Home Page", hotels=hotels,
                           hotel_names=hotel_names, hotel_cities=hotel_cities, hotel_states=hotel_states,
                           filter_key=filter_key, filter_val=filter_val,
                           )


@main.route("/about/")
def about():
    return render_template("about.html", title="About", block_title="About Page")
