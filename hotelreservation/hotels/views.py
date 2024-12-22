from flask import render_template, request, Blueprint, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from hotelreservation import db
from hotelreservation.hotels.forms import HotelForm
from hotelreservation.models import Hotel, Room, Reservation

hotels = Blueprint("hotels", __name__)


@hotels.route("/hotel/<int:hotel_id>/")
def hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template("hotel.html", title="Hotel", block_title="Hotel Page", hotel=hotel)


@hotels.route("/hotels/<string:name>/")
def hotel_rooms(name):
    print(f"method GET: {request.method == 'GET'}")
    print(f"method POST: {request.method == 'POST'}")
    page = request.args.get("page", 1, type=int)
    hotel = Hotel.query.filter_by(name=name).first_or_404()
    rooms = Room.query.filter_by(hotel=hotel).order_by(Room.price.desc()).paginate(page=page, per_page=5)
    return render_template("hotel_rooms.html", title="Hotel Rooms", block_title="Hotel Rooms Page", rooms=rooms, hotel=hotel)


@hotels.route("/hotels/<string:name>/")
def hotel_reservations(name):
    page = request.args.get("page", 1, type=int)
    hotel = Hotel.query.filter_by(name=name).first_or_404()
    reservations = Reservation.query.filter_by(hotel=hotel).order_by(Reservation.checkin_date.asc()).paginate(page=page, per_page=5)
    return render_template("hotel_reservations.html", title="Hotel Reservations", block_title="Hotel Reservations Page", reservations=reservations, hotel=hotel)


@hotels.route("/hotels/<int:hotel_id>/update/", methods=["GET", "POST"])
@login_required
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.author != current_user:
        abort(403)
    form = HotelForm()
    if form.validate_on_submit():
        hotel.title = form.title.data
        hotel.content = form.content.data
        db.session.commit()
        flash("Your hotel has been updated!", "success")
        return redirect(url_for("hotels.hotel", hotel_id=hotel.id))
    elif request.method == "GET":
        form.title.data = hotel.title
        form.content.data = hotel.content
    return render_template("create_hotel.html", title="Update Hotel", block_title="Update Hotel Page",
                           legend="Update Hotel Info", form=form)


@hotels.route("/hotels/<int:hotel_id>/delete/", methods=["POST"])
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.author != current_user:
        abort(403)
    db.session.delete(hotel)
    db.session.commit()
    flash("Your hotel has been deleted.", "success")
    return redirect(url_for("main.home"))
