from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

class UserModelTestCase(TestCase):
    """Tests for model for users. Runs before every test"""

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_user_input(self):
        user = User(first_name="TestUser", last_name="TestLastName", image_url="www.test.com")

        db.session.add(user)
        db.session.commit()

        user = User.query.get(firstname='TestUser')
        
