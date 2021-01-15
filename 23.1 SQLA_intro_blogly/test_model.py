from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Pets. Runs before every test"""
    def setUp(self):
        """Clean up any existing pets."""
        Pet.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_get_users(self):
        user = User(first_name="TestUser", last_name="TestLastName", image_url="www.test.com")
        db.session.add(user)
        db.session.commit()

        
