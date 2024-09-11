"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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


