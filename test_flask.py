from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    @classmethod
    def setUpClass(cls):
        """Set up the database and application context for the entire test class."""
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database and remove the application context after all tests in the class have run."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()

            user = User(first_name="Test", last_name="One")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "Test2", "image_url": "https://cdn.mos.cms.futurecdn.net/ASHH5bDmsp6wnK6mEfZdcU-1200-80.jpg.webp"}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2", html)

class PostTestCase(TestCase):
    """Tests for views for Users."""

    @classmethod
    def setUpClass(cls):
        """Set up the database and application context for the entire test class."""
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database and remove the application context after all tests in the class have run."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Add sample Post."""
        with app.app_context():
            User.query.delete()
            Post.query.delete()

            user = User(first_name="Test", last_name="One")
            post = Post(title="Test Title", content="this is test content")
            db.session.add(user)
            db.session.commit()
            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()


    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Title', html)
