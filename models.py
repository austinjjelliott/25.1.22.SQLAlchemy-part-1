"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func 

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User class"""
  __tablename__ = "users"
  
  def __repr__(self):
    p = self
    return f"<User id ={p.id} name = {p.first_name} {p.last_name}>"
  
  def greet(self):
    return f'Hi! I am {self.first_name} {self.last_name}'

  id = db.Column(db.Integer,
                 primary_key = True,
                 autoincrement = True)
  first_name = db.Column(db.String(25),
                         nullable = False)
  last_name = db.Column(db.String(30),
                        nullable = False)
  image_url = db.Column(db.String, 
                        nullable = True,
                        default = 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg')

  posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')


class Post(db.Model):
  """Posts that users can make. One to Many relationship"""
  __tablename__ = "posts"



  id = db.Column(db.Integer,
                 primary_key = True,
                 autoincrement = True)
  title = db.Column(db.String(25),
                    nullable = False)
  content = db.Column(db.String,
                      nullable = False)
  created_at = db.Column(db.DateTime, 
                           default=func.now(), 
                           nullable=True)  
  user_id = db.Column(db.Integer, 
                      db.ForeignKey('users.id'))

# 25.3 Additions....
#Relation to middle table 
  post_tags = db.relationship('PostTag', backref = 'post', cascade = 'all, delete-orphan')
  #relation to Tags (Many to Many)
  tags = db.relationship('Tag', secondary = 'posts_tags', backref = 'posts')



class Tag(db.Model):
  """add a TAG to your post. """
  __tablename__ = 'tags'


  id = db.Column(db.Integer, 
                 primary_key = True,
                 autoincrement = True)
  name = db.Column(db.Text, 
                   nullable = False,
                   unique = True)
  
  #Relation to middle table 
  tag_posts = db.relationship('PostTag', backref = 'tags', cascade = "all, delete-orphan")

class PostTag(db.Model):
  """Middle table combining the posts and the tags """

  __tablename__ = 'posts_tags'

  post_id = db.Column(db.Integer,
                      db.ForeignKey('posts.id'),
                      primary_key = True,
                      nullable = False)
  tag_id = db.Column(db.Integer, 
                     db.ForeignKey('tags.id'),
                     primary_key = True,
                     nullable = False)


