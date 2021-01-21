from models import User, Post, PostTag, Tag, db
from app import app


# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
bilbo = User(first_name='Bilbo', last_name="Baggins")
gandalf = User(first_name='Gandalf', last_name="White", image_url="www.whatthis.com")
leoglas = User(first_name='Leoglas', last_name="Elf")
sam = User(first_name="Sam", last_name="Wise")


# Add new objects to session, so they'll persist
db.session.add(bilbo)
db.session.add(gandalf)
db.session.add(leoglas)


# #Add some posts
post = Post(title="Middle Earth", content="Where is middle earth? We need to take the ring there")
sam.post.append(post)
db.session.add(sam)

sample1 = Tag(name="sample")

db.session.add(sample1)



# Commit--otherwise, this never gets saved!
db.session.commit()
