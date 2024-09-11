"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return redirect(f'/{new_user.id}')

# Details route - shows the details page for the user we click on 
@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details of a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user from DB"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/')

@app.route('/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_details.html', user = user)

@app.route('/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update user details in the DB"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()
    return redirect('/')