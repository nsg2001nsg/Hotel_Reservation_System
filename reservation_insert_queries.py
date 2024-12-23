import random
import datetime
from datetime import timedelta
from hotelreservation import db, create_app
from hotelreservation.models import Hotel, Room, Reservation, User

app = create_app()

# Example data for reservation table
reservation_types = ["Tentative", "Waitlisted", "Confirmed"]
reservations_per_room = 10  # Number of reservations per room

# Fetch all hotels
users = User.query.filter_by(
    super_user=False,
    staff_user=False,
).all()

# Fetch all hotels
hotels = Hotel.query.all()

# Generate reservations for each room
reservations = []
for hotel in hotels:
    # Fetch all rooms
    rooms = Room.query.filter_by(hotel=hotel)
    for room in rooms:
        for i in range(1, reservations_per_room + 1):
            date_posted = datetime.date.today() - timedelta(days=random.randint(0, 365))
            checkin_date = date_posted + timedelta(days=random.randint(0, 365))
            checkout_date = checkin_date + timedelta(days=random.randint(1, 8))
            payment_status = random.choice([True, False])
            if not bool(room.reservations.filter(Reservation.checkin_date == checkin_date).all()) and not payment_status:
                reservation_type = reservation_types[0]  # Tentative
                room.availability_status = True
            elif not bool(room.reservations.filter(Reservation.checkin_date == checkin_date).all()) and payment_status:
                reservation_type = reservation_types[2]  # Confirmed
                room.availability_status = False
            else:
                reservation_type = reservation_types[1]  # Waitlisted
            reservation = Reservation(
                number=f"{hotel.id}-{room.id}-{i:02d}",  # Reservation number format: hotel_id-room_number-reservation_number
                date_posted=date_posted,
                type=reservation_type,
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                payment_status=payment_status,
                guest_count=random.randint(1, room.capacity * 3),
                customer_id=random.choice(users).id,
                hotel_id=hotel.id,
                room_id=room.id,
            )
            reservations.append(reservation)

# Insert reservations into the database
db.session.add_all(reservations)
db.session.commit()

print(f"{len(reservations)} reservations added successfully!")
