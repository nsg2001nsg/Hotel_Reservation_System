from hotelreservation import db
from hotelreservation.models import User, Post

# db.create_all()  # create all models(tables)
# db.drop_all()  # drop all models(tables)

user1 = User(username="surajgupta", email="surajgupta@email.com", password="password")
db.session.add(user1)
db.session.commit()
user1 = User.query.filter_by(username="surajgupta").first()
post1 = Post(title="Blog Post 1", content="Blog Post 1 content", user_id=user1.id)
db.session.add(post1)
db.session.commit()
# user1.posts  # [Blog Post 1 - 2024-12-15 17:38:29.005847]
# post1.user_id  # 1

user2 = User(username="ojasrajvaidya", email="ojasrajvaidya@email.com", password="password")
db.session.add(user2)
db.session.commit()
user2 = User.query.filter_by(username="ojasrajvaidya").first()
post2 = Post(title="Blog Post 2", content="Blog Post 2 content", user_id=user2.id)
db.session.add(post2)
db.session.commit()
# user2.posts  # [Blog Post 2 - 2024-12-15 17:38:29.005847]
# post2.user_id  # 2

User.query.all()  # True
User.query.first()  # True
User.query.count()  # True
# user1 = User.query.filter_by(username="surajgupta").all()  # True
user1 = User.query.filter_by(username="surajgupta").first()  # True
User.query.get(1)  # True, deprecated, now available as Session.get()
User.query.get("1")  # True, deprecated, now available as Session.get()
db.session.get(User, 1)  # True, gets only by primary key id
db.session.get(User, "1")  # True, gets only by primary key id
User.query.delete()
User.query.update()

user = User.query.all()[1]
for i in range(1, 13):
    post = Post(title=f"Blog Post {i}", content=f"Blog Post {i} content", author=user)
    db.session.add(post)
db.session.commit()

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
s = Serializer("secret")
token = s.dumps({"user_id": "1"})
s.loads(token, max_age=30)
