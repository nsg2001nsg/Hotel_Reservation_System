import random
from datetime import datetime, timedelta
from hotelreservation import db, create_app
from hotelreservation.models import Hotel

app = create_app()

# Example data for hotel table
states_and_cities = [
    ("Rajasthan", ["Jaipur", "Jodhpur", "Udaipur"]),
    ("Goa", ["Panaji", "Vasco da Gama", "Mapusa"]),
    ("Himachal Pradesh", ["Shimla", "Manali", "Dharamshala"]),
    ("Maharashtra", ["Mumbai", "Pune", "Nagpur"]),
    ("Karnataka", ["Bangalore", "Mysore", "Mangalore"]),
    ("Tamil Nadu", ["Chennai", "Coimbatore", "Madurai"]),
    ("West Bengal", ["Kolkata", "Darjeeling", "Howrah"]),
    ("Kerala", ["Thiruvananthapuram", "Kochi", "Kozhikode"]),
    ("Delhi", ["New Delhi"]),
    ("Punjab", ["Amritsar", "Chandigarh", "Ludhiana"]),
]
hotel_types = ["Luxury", "Resort", "Boutique", "Business", "Homestay"]
descriptions = [
    "Experience unmatched luxury and elegance.",
    "Relax and rejuvenate in our tranquil haven.",
    "A perfect blend of comfort and convenience.",
    "Step into a world of heritage and charm.",
    "Tailored for business travelers and modern needs.",
]
image_files = [f"hotel{i}.jpg" for i in range(1, 21)]
prefixes = ["The Grand", "Cozy", "Seaside", "Heritage", "Hilltop", "Cityscape"]
suffixes = ["Palace", "Resort", "Inn", "Haven", "Homestay", "Retreat"]

# Generate 100 hotels
hotels = []
for i in range(1, 101):
    state, cities = random.choice(states_and_cities)
    city = random.choice(cities)
    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
    hotels.append(
        Hotel(
            name=name,
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 365)),
            type=random.choice(hotel_types),
            description=random.choice(descriptions),
            image_file=random.choice(image_files),
            city=city,
            state=state,
            contact=str(random.randint(7000000000, 9999999999)),
        )
    )

# Insert hotels into the database
db.session.add_all(hotels)
db.session.commit()

print(f"{len(hotels)} hotels added successfully!")
