from flask import render_template, request, Blueprint, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from hotelreservation import db
from hotelreservation.models import Room, Reservation
from hotelreservation.rooms.forms import ReservationForn

reservations = Blueprint("reservations", __name__)


@reservations.route("/reservation/<int:reservation_id>/")
def reservation(reservation_id):
    reservation = Room.query.get_or_404(reservation_id)
    return render_template("reservation.html", title="Reservation", block_title="Reservation Page", reservation=reservation)


@reservations.route("/reservations/<int:reservation_id>/update/", methods=["GET", "POST"])
@login_required
def update_reservation(reservation_id):
    reservation = Room.query.get_or_404(reservation_id)
    if reservation.author != current_user:
        abort(403)
    form = ReservationForn()
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
