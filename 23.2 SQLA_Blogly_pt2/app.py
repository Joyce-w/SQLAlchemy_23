from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    """Redirect to list of users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users')   
def get_users():
    """Shows all the users"""
    users = User.query.all()
    return render_template('users.html', users=users)

#---------------New User ROUTES -------------------------#

@app.route('/users/new')
def new_user_form():
    """Show users in database"""
    users = User.query.all()
    return render_template('new_user.html', users=users )

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

#---------------User details ROUTE -------------------------#

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Reterive and display data on user"""
    user = User.query.get_or_404(user_id)

    return render_template('detail.html', user=user)


#---------------User Edit ROUTES -------------------------#

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit user information"""
    users = User.query.filter(User.id == user_id).first()
    return render_template('edit_user.html', users=users)

# Edit user information (update in db)
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_info(user_id):
    """Edit user information"""

    #get user_id number
    user = User.query.get_or_404(user_id)

    #save input values
    edited_first = request.form["first_name"]
    edited_first = edited_first if edited_first else user.first_name


    edited_last = request.form["last_name"]
    edited_last = edited_last if edited_last else user.last_name

    edited_url = request.form["picture"]
    edited_url= edited_url if edited_url else user.image_url

    user.first_name = edited_first
    user.last_name = edited_last
    user.image_url = edited_url

    db.session.add(user)
    db.session.commit()
    
    # commit new data? 
    return redirect('/users')

#---------------User Deletion ROUTE ------------------#

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete current user from db"""

    del_user_id = request.form["delete"]

    user = User.query.filter_by(id=del_user_id).delete()
    db.session.commit()

    return redirect('/users')

#---------------POST ROUTES -------------------------#

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Directs to form for a new post"""
    return render_template('post.html')
    

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def user_post(user_id):
    """Directs to form for a new post"""
    user = User.query.get_or_404(user_id)

    post_title = request.form["title"]
    post_content = request.form["content"]
    post_datetime = datetime.now()
    user_posted = user.id

    new_post = Post(title=post_title, content=post_content, created_at =post_datetime, user_id=user_posted)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")
