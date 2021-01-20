from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for users. Runs before every test"""

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_user_input(self):
        test_user= User(first_name="Alpha1", last_name="Alpha2")
        
    db.session.add(test_user)
    db.session.commit()