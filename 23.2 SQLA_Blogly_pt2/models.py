"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    #define table name in db
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id ={u.id} first_name = {u.first_name} last_name = {u.last_name}>"

    #define indiv col in users table 
    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
                
    #define first name col in users table
    first_name = db.Column(db.String(20),
                nullable = True)

    #define last_name col in users table
    last_name = db.Column(db.String(20))

    #define col for image url
    image_url = db.Column(db.String)    

class Post(db.Model):
    #Create model for blog posts
    __tablename__ = "post"

    # def __repr__(self):
    #     p = self
    #     return f"<Post >"

    #define pk col for post table
    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    
    #define title col for post table
    title = db.Column(db.String(50),
                nullable=True)
    
    #define desc content for post table
    content = db.Column(db.String(250))
        
    #create timestamp for post table 
    created_at = db.Column(db.DateTime(),
                nullable=True)
    
    #FK for User.id
    user_id = db.Column(db.Integer,
                db.ForeignKey('users.id'))