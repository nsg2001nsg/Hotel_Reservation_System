import datetime
from datetime import timedelta

from flask import render_template, request, Blueprint, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import Date

from hotelreservation import db
from hotelreservation.models import Room, Reservation, Hotel
from hotelreservation.reservations.forms import ReservationForm

reservations = Blueprint("reservations", __name__)

reservation_types = ["Tentative", "Waitlisted", "Confirmed"]


@reservations.route("/reservation/<int:reservation_id>/")
def reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    return render_template("reservation.html", title="Reservation", block_title="Reservation Page", reservation=reservation, room=reservation.room_id)


@reservations.route("/reservations/<int:room_id>/create/", methods=["GET", "POST"])
@login_required
def create_reservation(room_id):
    room = Room.query.filter_by(id=room_id).first_or_404()
    hotel = Hotel.query.filter_by(id=room.hotel_id).first_or_404()
    last_reservation = Reservation.query.order_by(Reservation.id.desc()).first()
    form = ReservationForm()
    number = f"{hotel.id}-{room.id}-{last_reservation.id + 1:02d}"
    if form.validate_on_submit():
        last_reservation = Reservation.query.order_by(Reservation.id.desc()).first()
        number = f"{hotel.id}-{room.id}-{last_reservation.id+1:02d}"  # Reservation number format: hotel_id-room_number-reservation_number
        # checkin_date = date_posted + timedelta(days=random.randint(0, 365))
        # checkout_date = checkin_date + timedelta(days=random.randint(1, 8))
        # reservation = Reservation(title=form.title.data, content=form.content.data, author=current_user, hotel_id=room_id.hotel_id, room_id=room.id)
        # db.session.add(reservation)
        # db.session.commit()
        flash("Your reservation has been created.", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        checkin_date = datetime.date.today() + timedelta(days=8)
        print(checkin_date)
        # import ipdb; ipdb.set_trace()
        if not bool(room.reservations.filter(Reservation.checkin_date == checkin_date).all()):
            reservation_type = reservation_types[0]  # Tentative
        else:
            reservation_type = reservation_types[1]  # Waitlisted
        form.type.data = reservation_type
        form.checkin_date.data = checkin_date
        # form.checkout_date.data = checkin_date + timedelta(days=1)
        # form.guest_count.data = 1
    return render_template("create_reservation.html", title="Create Reservation", block_title="Create Reservation Page",
                           legend="Create Reservation Info", hotel=hotel, room=room, form=form)


@reservations.route("/reservations/<int:reservation_id>/update/", methods=["GET", "POST"])
@login_required
def update_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.author != current_user:
        abort(403)
    form = ReservationForm()
    if form.validate_on_submit():
        reservation.title = form.title.data
        reservation.content = form.content.data
        db.session.commit()
        flash("Your reservation has been updated!", "success")
        return redirect(url_for("reservations.reservation", reservation_id=reservation.id))
    elif request.method == "GET":
        form.title.data = reservation.title
        form.content.data = reservation.content
    return render_template("create_reservation.html", title="Update Hotel", block_title="Update Hotel Page",
                           legend="Update Hotel Info", form=form)


@reservations.route("/reservations/<int:reservation_id>/delete/", methods=["POST"])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.author != current_user:
        abort(403)
    db.session.delete(reservation)
    db.session.commit()
    flash("Your reservation has been deleted.", "success")
    return redirect(url_for("main.home"))
