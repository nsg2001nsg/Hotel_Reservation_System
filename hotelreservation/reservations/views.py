import datetime
from datetime import timedelta

from flask import render_template, request, Blueprint, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from hotelreservation import db
from hotelreservation.models import Room, Reservation, Hotel
from hotelreservation.reservations.forms import ReservationForm
from hotelreservation.users.utils import send_reservation_email

reservations = Blueprint("reservations", __name__)

reservation_types = ["Tentative", "Waitlisted", "Confirmed"]


@reservations.route("/reservation/<int:reservation_id>/")
def reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    return render_template("reservation.html", title="Reservation", block_title="Reservation Page", reservation=reservation, room=reservation.room)


@reservations.route("/reservations/<int:room_id>/create/", methods=["GET", "POST"])
@login_required
def create_reservation(room_id):
    room = Room.query.get_or_404(room_id)
    hotel = Hotel.query.get_or_404(room.hotel.id)
    form = ReservationForm()
    if form.validate_on_submit():
        last_reservation = Reservation.query.order_by(Reservation.id.desc()).first()
        reservation = Reservation(
            number=f"{hotel.id}-{room.id}-{last_reservation.id+1:02d}",  # Reservation number format: hotel_id-room_number-reservation_number
            type=form.type.data,
            checkin_date=form.checkin_date.data,
            checkout_date=form.checkout_date.data,
            guest_count=form.guest_count.data,
            customer=current_user,
            hotel=hotel,
            room=room,
        )
        db.session.add(reservation)
        db.session.commit()
        flash(f"Your reservation has been created. Booking Status: {form.type.data}.", "success")
        send_reservation_email(current_user, form.type.data)
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        checkin_date = datetime.date.today() + timedelta(days=1)
        if not bool(room.reservations.filter(Reservation.checkin_date == checkin_date).all()):
            reservation_type = reservation_types[0]  # Tentative
        else:
            reservation_type = reservation_types[1]  # Waitlisted
        form.type.data = reservation_type
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
        reservation.type = form.type.data
        reservation.guest_count = form.guest_count.data
        db.session.commit()
        flash("Your reservation has been updated!", "success")
        return redirect(url_for("reservations.reservation", reservation_id=reservation.id))
    elif request.method == "GET":
        form.type.data = reservation.type
        form.guest_count.data = reservation.guest_count
    return render_template("create_reservation.html", title="Update Reservation", block_title="Update Reservation Page",
                           legend="Update Reservation Info", form=form)


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
