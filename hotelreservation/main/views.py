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
    print(f"request.args: {request.args}")
    page = request.args.get("page", 1, type=int)
    if request.method == "POST":
        print(f"request.form: {request.form}")
        select_name = request.form.getlist("name")
        select_city = request.form.getlist("city")
        select_state = request.form.getlist("state")
        print(f"select_name: {select_name}")
        print(f"select_city: {select_city}")
        print(f"select_state: {select_state}")
        filter_value = max([select_name, select_city, select_state])
        print(f"filter_value: {filter_value}")
        filter_ind = [select_name, select_city, select_state].index(filter_value)
        print(f"filter_ind: {filter_ind}")
        filters_list = [
            {"name": request.form.get("name", "")},
            {"city": request.form.get("city", "")},
            {"state": request.form.get("state", "")},
        ]
        print(f"filters_list: {filters_list}")
        filters = filters_list[filter_ind]
        print(f"filters: {filters}")
        filter_keys = filters.keys()
        print(f"filter_keys: {filter_keys}")
        filter_key = list(filter_keys)[0] if filter_keys else None
        print(f"filter_key: {filter_key}")
        filter_values = filters.values()
        print(f"filter_values: {filter_values}")
        filter_value = list(filters.values())[0] if filters.values() else None
        print(f"filter_value: {filter_value}")
    else:
        filter_key = request.args.get("filter_key", "", type=str)
        print(f"filter_key: {filter_key}")
        filter_value = request.args.get("filter_value", "", type=str)
        print(f"filter_value: {filter_value}")
    filters = {filter_key: filter_value} if filter_key and filter_value else {}
    print(f"filters: {filters}")
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
                           filter_key=filter_key, filter_value=filter_value,
                           )


@main.route("/about/")
def about():
    return render_template("about.html", title="About", block_title="About Page")
