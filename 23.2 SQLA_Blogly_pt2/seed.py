from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
tes1 = User(first_name='TEST1FIRST', last_name="dog1")
bowser = User(first_name='TEST2FIRST', last_name="dog", image_url="www.whatthis.com")
spike = User(first_name='TEST3FIRST', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(tes1)
db.session.add(bowser)
db.session.add(spike)

#Add some posts

# Commit--otherwise, this never gets saved!
db.session.commit()
