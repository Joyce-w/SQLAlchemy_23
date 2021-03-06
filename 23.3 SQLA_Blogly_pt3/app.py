from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag
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

    return render_template('user_details.html', user=user)


#---------------User Edit ROUTES -------------------------#

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit user information"""
    users = User.query.filter(User.id == user_id).first()
    return render_template('edit_user.html', users=users)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_info(user_id):
    """Edit user information, update to db"""

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

    tag_list = Tag.query.all()

    return render_template('post_form.html', tag_list=tag_list)
    

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def user_post(user_id):
    """Directs to form for a new post"""

    # Get post information
    user = User.query.get_or_404(user_id)

    post_title = request.form["title"]
    post_content = request.form["content"]
    post_datetime = datetime.now()
    user_posted = user.id

    new_post = Post(title=post_title, content=post_content, created_at =post_datetime, user_id=user_posted)
    

    # get tag information    
    tag_option = request.form.getlist("tags")
        
    # query db for tags, returns list of queries
    tags = Tag.query.filter(Tag.id.in_(tag_option)).all()
    
    # loop thru 
    for tag in tags:
        new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()


    return redirect(f"/users/{user_id}")


@app.route("/users/posts/<int:post_id>")
def post_details(post_id):
    """Show page for particular posting"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', post=post)


@app.route("/users/posts/<int:post_id>/edit")
def post_edit(post_id):
    """Route to edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_edit.html", post=post)

@app.route("/users/posts/<int:post_id>/edit", methods=["POST"])
def post_update_edits(post_id):
    """Updates post edits to db"""

    #get post information from db
    post = Post.query.get_or_404(post_id)

    # save input values
    
    e_title = request.form["title"]
    e_title = e_title if e_title else post.title

    e_content = request.form["content"]
    e_content = e_content if e_content else post.content

    e_datetime = datetime.now()

    #Make changes to session
    post.title = e_title
    post.content = e_content
    post.created_at = e_datetime

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/users/posts/{post.id}")

@app.route("/users/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete route for route"""

    del_post_id = request.form["delete"]

    post = Post.query.filter_by(id=del_post_id).delete()
    db.session.commit()

    return redirect('/users')




# -------------------Tags Route--------------------------#
@app.route('/tags')
def list_tags():
    """Display list of tags being used"""
    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show information about a particular tag"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/new')
def new_tag():
    """Show a form to add a new tag"""

    return render_template('tag_form.html')

@app.route('/tags/new', methods=["POST"])
def get_tag():
    """Retrieve submitted data"""
    new_tag = request.form["new_tag"]
    
    tag = Tag(name=new_tag)
    
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """Show edit form for a tag"""
    
    #get post information from db
    tag = Tag.query.get_or_404(tag_id)

    # save input values
    edit_tag = request.form["tag"]
    edit_tag = edit_tag if edit_tag else tag.name

    #Make changes to session
    tag.name = edit_tag

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def dete_tag(tag_id):
    """Delete Tag from db"""

    delete_tag = request.form["delete"]

    tag = Tag.query.filter_by(id=delete_tag).delete()

    db.session.commit()

    return redirect('/tags')


