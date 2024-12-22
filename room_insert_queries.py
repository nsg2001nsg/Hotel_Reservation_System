import random
from datetime import datetime, timedelta
from hotelreservation import db, create_app
from hotelreservation.models import Hotel, Room

app = create_app()

# Example data for room table
room_types = {
    "Single": {"capacity": 1, "price": 1500},
    "Double": {"capacity": 2, "price": 3000},
    "Suite": {"capacity": 3, "price": 4500},
    "Deluxe": {"capacity": 4, "price": 6000},
}
descriptions = [
    "Experience unmatched luxury and elegance.",
    "Relax and rejuvenate in our tranquil haven.",
    "A perfect blend of comfort and convenience.",
    "Step into a world of heritage and charm.",
    "Tailored for business travelers and modern needs.",
]
image_files = [f"room{i}.jpg" for i in range(1, 21)]
rooms_per_hotel = 10  # Number of rooms per hotel

# Fetch all hotels
hotels = Hotel.query.all()

# Generate rooms for each hotel
rooms = []
for hotel in hotels:
    for i in range(1, rooms_per_hotel + 1):
        room_type = random.choice(list(room_types.keys()))
        room_data = room_types[room_type]
        room = Room(
            number=f"{hotel.id}-{i:02d}",  # Room number format: hotel_id-room_number
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 365)),
            type=room_type,
            description=random.choice(descriptions),
            image_file=random.choice(image_files),
            availability_status=random.choice([True, False]),
            price=room_data["price"],
            capacity=room_data["capacity"],
            hotel_id=hotel.id,
        )
        rooms.append(room)

# Insert rooms into the database
db.session.add_all(rooms)
db.session.commit()

print(f"{len(rooms)} rooms added successfully!")
