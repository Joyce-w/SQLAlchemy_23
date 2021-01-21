from models import User, Post, PostTag, Tag, db
from app import app


# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
bilbo = User(first_name='Bilbo', last_name="Baggins", image_url="https://static.wikia.nocookie.net/lotr/images/b/b6/The_Hobbit_wallpaper_48.jpg")
gandalf = User(first_name='Gandalf', last_name="White", image_url="https://cms.qz.com/wp-content/uploads/2018/08/gandalf-lord-of-the-rings-e1534255368438.jpg")
leoglas = User(first_name='Leoglas', last_name="Elf", image_url="https://i.pinimg.com/originals/04/80/29/048029f362c484a2a46b928afbe98837.jpg")
sam = User(first_name="Sam", last_name="Wise", image_url="https://static.wikia.nocookie.net/lotr/images/2/20/Sam.jpg")


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
