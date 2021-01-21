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

    # Reference to Post(1-to-1)
    post = db.relationship('Post',
                    backref="users",
                    cascade="all,delete")
    

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
    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<User id ={p.id} title = {p.title} content = {p.content}>"

    # Relation between Post and PostTag
    tags = db.relationship('Tag',
                secondary="posttags",
                backref="posts")

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

class PostTag(db.Model):

    # creat table name
    __tablename__ = "posttags"

    def __repr__(self):
        pt = self
        return f"<PostTag post_id ={pt.post_id}, tag_id = {pt.tag_id}>"

    # define post_id
    post_id = db.Column(db.Integer,
                db.ForeignKey('posts.id'),
                primary_key=True,
                nullable=True)

    tag_id = db.Column(db.Integer,
                db.ForeignKey('tags.id'),
                primary_key=True,
                nullable=True)


class Tag(db.Model):
    # creat table name
    __tablename__ = "tags"
    
    def __repr__(self):
        t = self
        return f"<Tag id ={t.id}, name = {t.name}>"

    posttag = db.relationship('PostTag', backref="tags")

    # define id
    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
        
    # define unique name column        
    name = db.Column(db.Text,
                nullable=True,
                unique=True)    

    
