from flask import render_template, request, Blueprint, redirect, flash, url_for, abort
from flask_login import current_user, login_required

from hotelreservation import db
from hotelreservation.models import Room, Reservation
from hotelreservation.rooms.forms import RoomForm

rooms = Blueprint("rooms", __name__)


@rooms.route("/room/<int:room_id>/")
def room(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template("room.html", title="Room", block_title="Room Page", room=room)


@rooms.route("/rooms/<int:room_id>/")
def room_reservations(room_id):
    page = request.args.get("page", 1, type=int)
    room = Room.query.get_or_404(room_id)
    reservations = Reservation.query.filter_by(room=room).order_by(Reservation.checkin_date.asc()).paginate(page=page, per_page=5)
    # reservations = Reservation.query.filter_by(room=room).group_by(room.type).order_by(Reservation.checkin_date.asc()).paginate(page=page, per_page=5)
    return render_template("room_reservations.html", title="Room Reservations", block_title="Room Reservations Page", reservations=reservations, room=room)


@rooms.route("/rooms/create/", methods=["GET", "POST"])
@login_required
def create_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(room)
        db.session.commit()
        flash("Your room has been created.", "success")
        return redirect(url_for("main.home"))
    return render_template("create_room.html", title="Create Room", block_title="Create Room Page",
                           legend="Create Room Info", form=form)


@rooms.route("/rooms/<int:room_id>/update/", methods=["GET", "POST"])
@login_required
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    if room.author != current_user:
        abort(403)
    form = RoomForm()
    if form.validate_on_submit():
        room.title = form.title.data
        room.content = form.content.data
        db.session.commit()
        flash("Your room has been updated!", "success")
        return redirect(url_for("rooms.room", room_id=room.id))
    elif request.method == "GET":
        form.title.data = room.title
        form.content.data = room.content
    return render_template("create_room.html", title="Update Room", block_title="Update Room Page",
                           legend="Update Room Info", form=form)


@rooms.route("/rooms/<int:room_id>/delete/", methods=["POST"])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if room.author != current_user:
        abort(403)
    db.session.delete(room)
    db.session.commit()
    flash("Your room has been deleted.", "success")
    return redirect(url_for("main.home"))
