"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
@app.route('/users/<int:user_id>/posts/<int:post_id>/')
def show_post(user_id, post_id):    
    """Show details of a single post """
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template ('posts.html', user = user, post = post, tags = tags)

#GET /users/[user-id]/posts/new : Show form to add a post for that user.
@app.route('/users/<int:user_id>/posts/new')
def make_a_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('make_a_post.html', user = user, tags = tags)

#POST THE POST: POST /users/[user-id]/posts/new : Handle add form; add post and redirect to the user detail page.
@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def post_the_post(user_id):
    user = User.query.get_or_404(user_id)

    # Create the new post 
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title = title, content = content, user_id = user.id)    
    db.session.add(new_post)
    db.session.commit()
    #  Add the tags to this newly created post 
    tag_ids = request.form.getlist('tags[]')
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        if tag: 
            new_post.tags.append(tag)
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
    tagged_tags = post.tags
    tags = Tag.query.all()
    return render_template("edit_post.html", user = user, post = post, tagged_tags = tagged_tags, tags = tags)

#Post the editted post info to the database and return to the user's details page 
@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods = ["POST"])
def update_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    #get the list of current tags on the post 
    current_tag_ids = [tag.id for tag in post.tags]
    #Get the list of tags submitted on the form: Note! Needs to be done in [int(tag_id) etc] cuz the form will submit strings automatically, NOT integers! So need to first convert 
    tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags[]')]
    #Add ONLY the new tags 
    for tag_id in tag_ids: 
        if tag_id not in current_tag_ids:
            tag = Tag.query.get(tag_id)
            if tag: 
                post.tags.append(tag)
    #Remove tags that were unchecked in the form 
    for tag_id in current_tag_ids:
        if tag_id not in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag: 
                post.tags.remove(tag)
    #commit these changes to the DB: 
    db.session.commit() 



    return redirect(f'/users/{user_id}')

#ADDING NEW ROUTES FOR 25.3 
@app.route("/tags")
def show_tags():
    tags = Tag.query.all()
    return render_template ('tag_lists.html', tags = tags)

#GET /tags/[tag-id] : Show detail about a tag. Have links to edit form and to delete.
@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts   
    return render_template('tag_details.html', tag = tag, posts = posts)

# New TAG Route - adds new TAG to DB from info typed into the form 
@app.route('/tags', methods = ["POST"])
def create_tag():
    name = request.form['name']

    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f'/tags/{new_tag.id}')

# GET /tags/[tag-id]/edit : Show edit form for a tag.
@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag = tag)

#POST /tags/[tag-id]/edit : Process edit form, edit tag, and redirects to the tags list.
@app.route("/tags/<int:tag_id>/edit", methods = ["POST"])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect(f"/tags")

# POST /tags/[tag-id]/delete : Delete a tag.
@app.route('/tags/<int:tag_id>/delete', methods = ["POST"])
def delete_tag(tag_id):
    """Delete a tag from the database """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect ('/tags')
