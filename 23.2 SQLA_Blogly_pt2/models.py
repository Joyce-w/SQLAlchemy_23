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
        p = self
        return f"<User id ={p.id} first_name = {p.first_name} last_name = {p.last_name}>"

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