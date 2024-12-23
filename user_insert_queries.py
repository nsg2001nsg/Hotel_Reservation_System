import random
from hotelreservation import bcrypt, db, create_app
from hotelreservation.models import User

app = create_app()

# Example data for hotel table

first_name = ["suraj", "ojas", "vishal", "gyan", "ankit", "anil"]
last_name = ["gupta", "rajvaidya", "singh", "chauhan", "singh", "pradhan"]

password = "password"

# Generate users
users = list()
users.append(
    User(
        username="surajsgupta0107",
        email="surajsgupta0107@gmail.com",
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
        contact=str(random.randint(7000000000, 9999999999)),
        super_user=True,
        staff_user=True,
    )
)
users.append(
    User(
        username="sgcorp0107",
        email="sgcorp0107@gmail.com",
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
        contact=str(random.randint(7000000000, 9999999999)),
        super_user=True,
        staff_user=True,
    )
)
for i in range(len(first_name)):
    username = f"{first_name}{last_name}"
    users.append(
        User(
            username=f"{first_name[i]}{last_name[i]}",
            email=f"{first_name[i]}{last_name[i]}@gmail.com",
            password=bcrypt.generate_password_hash(password).decode("utf-8"),
            contact=str(random.randint(7000000000, 9999999999)),
        )
    )

# Insert hotels into the database
db.session.add_all(users)
db.session.commit()

print(f"{len(users)} users added successfully!")
