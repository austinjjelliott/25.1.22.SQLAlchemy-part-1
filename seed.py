from models import User, Post, db
from app import app


with app.app_context():  #THIS LINE IS KEY!! I always need it, and it is always left out of the videos! Find out why please...
#Create Tables...
    db.drop_all()
    db.create_all()
#Create Variables to fill the tables
    user1 = User(first_name = "Austin", last_name = "Elliott", image_url = "https://media.istockphoto.com/id/508283104/photo/close-up-of-a-chihuahua-in-front-of-a-pink-background.webp?s=1024x1024&w=is&k=20&c=0_nxl_peQFv0q3ZpK1nxf2vHoMle0o-EOEOWW52vwcw=")
    user2 = User(first_name = "Justin", last_name = "Elliott", image_url = "https://media.istockphoto.com/id/508283104/photo/close-up-of-a-chihuahua-in-front-of-a-pink-background.webp?s=1024x1024&w=is&k=20&c=0_nxl_peQFv0q3ZpK1nxf2vHoMle0o-EOEOWW52vwcw=")
    user3 = User(first_name = "Dustin", last_name = "Elliott", image_url = "https://media.istockphoto.com/id/508283104/photo/close-up-of-a-chihuahua-in-front-of-a-pink-background.webp?s=1024x1024&w=is&k=20&c=0_nxl_peQFv0q3ZpK1nxf2vHoMle0o-EOEOWW52vwcw=")
    user4 = User(first_name = "Rustin", last_name = "Elliott", image_url = "https://media.istockphoto.com/id/508283104/photo/close-up-of-a-chihuahua-in-front-of-a-pink-background.webp?s=1024x1024&w=is&k=20&c=0_nxl_peQFv0q3ZpK1nxf2vHoMle0o-EOEOWW52vwcw=")


    post1 = Post(title = "Post 1", content = "First post", user_id = 1)
    post2 = Post(title = "Post 2", content = "Second post", user_id = 1)
    post3 = Post(title = "Post 3", content = "Third post", user_id = 1)
    post4 = Post(title = "Post 1", content = "First post", user_id = 2)
    post5 = Post(title = "Post 2", content = "Second post", user_id = 2)
    post6 = Post(title = "Post 3", content = "Third post", user_id = 2)
    post7 = Post(title = "Post 1", content = "First post", user_id = 3)


#Add the departments to the departments table
    db.session.add_all([user1, user2, user3, user4])
#Commit them! This has to be here cuz if you dont commit the departents 
# first you cant add the employees whose dept_code is required to be in the
# departents table 
    db.session.commit() 
#Add and commit the employees 
    db.session.add_all([post1,post2,post3,post4,post5,post6,post7])
    db.session.commit()