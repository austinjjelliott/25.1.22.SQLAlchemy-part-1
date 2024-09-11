from unittest import TestCase
from app import app
from models import User, db

# Use a test database to avoid cluttering tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False 

class UserModelTestCase(TestCase):
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
        """Create a new user instance before each test."""
        self.user = User(first_name="Test", last_name="One")

    def test_greet_method(self):
        """Test the greet method of the User model."""
        self.assertEqual(self.user.greet(), "Hi! I am Test One")

    def tearDown(self):
        """Roll back any changes to the database."""
        with app.app_context():
            db.session.rollback()
