from models import User, Post, Tag, PostTag, db
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


    post1 = Post(title = "Post 1", content = "Funny post", user_id = 1)
    post2 = Post(title = "Post 2", content = "Funny post", user_id = 1)
    post3 = Post(title = "Post 3", content = "Cringe post", user_id = 1)
    post4 = Post(title = "Post 1", content = "Wholesome post", user_id = 2)
    post5 = Post(title = "Post 2", content = "Another Wholesome post", user_id = 2)
    post6 = Post(title = "Post 3", content = "Funny post", user_id = 2)
    post7 = Post(title = "Post 1", content = "No Tag post", user_id = 3)

    tag1 = Tag(name = 'Funny', 
               tag_posts = [PostTag(post_id = 1, tag_id = 1),
                            PostTag(post_id = 2, tag_id = 1),
                            PostTag(post_id = 6, tag_id = 1)])
    tag2 = Tag(name = 'Cringe',
               tag_posts = [PostTag(post_id = 3, tag_id = 2)])
    tag3 = Tag(name = 'Wholesome',
               tag_posts = [PostTag(post_id = 4, tag_id = 3),
                            PostTag(post_id = 5, tag_id = 3)])


#Add the users to the users table
    db.session.add_all([user1, user2, user3, user4])
#Commit them! This has to be here cuz if you dont commit the users 
# first you cant add the posts whose user_id is required to be in the
#  table 
    db.session.commit() 
#Add and commit the posts 
    db.session.add_all([post1,post2,post3,post4,post5,post6,post7])
    db.session.commit()

#add and commit the tags 
    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()