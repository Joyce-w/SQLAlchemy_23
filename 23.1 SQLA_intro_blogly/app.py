from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

@app.route('/users/new')
def new_user_form():
    """Show users in database"""
    users = User.query.all()
    return render_template('new_user.html', users=users )

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Reterive and display data on user"""
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)