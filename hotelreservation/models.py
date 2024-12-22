from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

from hotelreservation import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    super_user = db.Column(db.Boolean, nullable=False, default=False)
    staff_user = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    reservations = db.relationship("Reservation", backref="customer", lazy="dynamic")

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=180):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.username} - {self.email}"

    def __str__(self):
        return f"{self.username} - {self.email}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.date_posted}"

    def __str__(self):
        return f"{self.title} - {self.date_posted}"


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    rooms = db.relationship("Room", backref="hotel", lazy=True)
    reservations = db.relationship("Reservation", backref="hotel", lazy="dynamic")

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.type}"

    def __str__(self):
        return f"{self.id} - {self.name} - {self.type}"


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    availability_status = db.Column(db.Boolean, nullable=False, default=True)
    price = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"), nullable=False)
    reservations = db.relationship("Reservation", backref="room", lazy="dynamic")

    def __repr__(self):
        return f"{self.id} - {self.number} - {self.type} - {self.availability_status} - {self.price}"

    def __str__(self):
        return f"{self.id} - {self.number} - {self.type} - {self.availability_status} - {self.price}"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)
    checkin_date = db.Column(db.DateTime, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    guest_count = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.number} - {self.type} - {self.payment_status}"

    def __str__(self):
        return f"{self.id} - {self.number} - {self.type} - {self.payment_status}"
