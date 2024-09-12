"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  I dont think this is needed anymore...
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()  only need to do this once, done in terminal...

# Home route -- list all users
@app.route('/')
def list_users():
    users = User.query.all()
    return render_template ('lists.html', users = users)

# New User Route - adds new user to DB from info typed into the form 
@app.route('/', methods = ["POST"])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name= first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

# Details route - shows the details page for the user we click on 
@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details of a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('details.html', user=user, posts=posts)

#Delete a user route 
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user from DB"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/')

#Show the form to edit a user route 
@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_details.html', user = user)

#Post the editted user info to the database and return to the home screen
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update user details in the DB"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()
    return redirect('/')

#Show the Post details for one specific post at a time 
@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(user_id, post_id):    
    """Show details of a single post """
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template ('posts.html', user = user, post = post)

#GET /users/[user-id]/posts/new : Show form to add a post for that user.
@app.route('/users/<int:user_id>/posts/new')
def make_a_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('make_a_post.html', user = user)

#POST THE POST: POST /users/[user-id]/posts/new : Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def post_the_post(user_id):
    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    new_post = Post(title = title, content = content, user_id = user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

#Delete a POST route 
@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(user_id, post_id):
    """Deletes the POST from DB"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect (f'/users/{user_id}')

#Show the form to edit a user's POST
@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def edit_post_form(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", user = user, post = post)

#Post the editted post info to the database and return to the user's details page 
@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods = ["POST"])
def update_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/users/{user_id}')
